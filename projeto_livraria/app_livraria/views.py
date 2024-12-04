from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Livro, Autor, Autor_livro, Comentario, Genero_literario

def loginPage(request):
    page = 'login'
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')

        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "O usuário não existe :(")

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Usuário ou senha incorretos :(")

    context = {'page': page}
    return render(request, 'login_registro.html', context)

def logoutUser(request):
    logout(request)
    return redirect('home')

def registerPage(request):
    form = UserCreationForm()
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, 'Ocorreu um erro durante o cadastro!')

    return render(request, 'login_registro.html', {'form': form}) 

def home(request):
    search_query = request.GET.get('pesquisar', '').strip()
    generos_selecionados = request.GET.getlist('q')
    livros = Livro.objects.all()

    if generos_selecionados:
        livros = Livro.objects.filter(generos__genero__nome__in = generos_selecionados).distinct()
    
    if search_query:
        livros = livros.filter(
            Q(titulo__istartswith = search_query) |
            Q(autores__autor__nome__istartswith = search_query) |
            Q(generos__genero__nome__istartswith = search_query)
            ).distinct()
    
    livro_count = livros.count()

    livros = livros.order_by('titulo')
    context = {
        'livros': livros,
        'generos': Genero_literario.objects.all(),
        'generos_selecionados': generos_selecionados,
        'search_query': search_query,
        'livro_count':livro_count,
    }
    return render(request,'home.html', context)

def livro(request, pk):
    livro = Livro.objects.get(id=pk)
    if request.method == 'POST':
        Comentario.objects.create(
            user = request.user,
            livro = livro,
            mensagem = request.POST.get('mensagem'),
        )

    autores_livros = Autor_livro.objects.filter(livro=livro).select_related('autor')
    autores = [autor_livro.autor for autor_livro in autores_livros]

    novo_comentario = Comentario()
    novo_comentario.livro = livro
    novo_comentario.mensagem = request.POST.get('mensagem')
    #novo_comentario.user = 
    novo_comentario.save

    comentarios = Comentario.objects.filter(livro=livro)

    context = {
        'livro': livro,
        'autores': autores,
        'comentarios': comentarios,
    }
    return render(request, 'livro.html', context)