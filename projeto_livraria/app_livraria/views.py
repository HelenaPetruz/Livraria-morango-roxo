from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Q
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import UserCreationForm
from .models import Livro, Autor, Autor_livro, Comentario, Genero_literario, Pasta, Pasta_livro

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
    
    if request.user.is_authenticated:
        pastas = Pasta.objects.filter(user = request.user)
    else:
        pastas = None

    if request.method == 'POST':
        livro_id = request.POST.get('livro_id')
        livro = get_object_or_404(Livro, id=livro_id)
        pasta_ids = request.POST.getlist('pastas')
        for pasta_id in pasta_ids:
            pasta = get_object_or_404(Pasta, id=pasta_id)
            Pasta_livro.objects.create(livro=livro, pasta=pasta)
    return redirect('home')
    

    livro_count = livros.count()

    livros = livros.order_by('titulo')

    context = {
        'livros': livros,
        'generos': Genero_literario.objects.all(),
        'generos_selecionados': generos_selecionados,
        'search_query': search_query,
        'livro_count':livro_count,
    }
    if pastas is not None:
        context['pastas'] = pastas
    return render(request,'home.html', context)

def livro(request, pk):
    livro = Livro.objects.get(id=pk)
    if request.method == 'POST':
        Comentario.objects.create(
            user = request.user,
            livro = livro,
            mensagem = request.POST.get('mensagem'),
        )
        return redirect('livro', pk = livro.id)

    autores_livros = Autor_livro.objects.filter(livro=livro).select_related('autor')
    autores = [autor_livro.autor for autor_livro in autores_livros]

    comentarios = Comentario.objects.filter(livro=livro).order_by('-created')
    usuarios_unicos = User.objects.filter(comentario__livro=livro).distinct()

    context = {
        'livro': livro,
        'autores': autores,
        'comentarios': comentarios,
        'usuarios_unicos': usuarios_unicos.distinct(),
    }
    return render(request, 'livro.html', context)

@login_required(login_url='login')
def deleteComentario(request, pk):
    comentario = Comentario.objects.get(id=pk)

    if request.user != comentario.user:
        return HttpResponse('Você não tem acesso à essa página!')

    if request.method == 'POST':
        comentario.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj': comentario})

@login_required(login_url='login')
def editarComentario(request, comentario_id):
    comentario = get_object_or_404(Comentario, id=comentario_id)

    if request.user != comentario.user:
        return HttpResponse('Você não tem acesso à essa página!')
    
    if request.method == "POST":
        mensagem = request.POST.get("mensagem")
        comentario.mensagem = mensagem
        comentario.save() 
        return redirect('home')
    
    #pra caso method==get
    return render(request, 'editar_comentario.html', {'comentario_editing': comentario})

@login_required(login_url='login')
def pastas(request):
    pastas = Pasta.objects.filter(user=request.user).order_by('-created')
    return render(request, 'pastas.html', {'pastas': pastas})

@login_required(login_url='login')
def criarPasta(request):
    is_private = request.POST.get('visibilidade') == 'privado' #retorna true(privado) ou false(publico)
    if request.method == 'POST':
        if 'capa' in request.FILES:
            capa = request.FILES.get('capa')
        else:
            capa = 'capas_pastas/default.png'
        Pasta.objects.create(
            user = request.user,
            titulo = request.POST.get('titulo'),
            descricao = request.POST.get('descricao'),
            capa = capa,
            is_private = is_private
        )
        return redirect('pastas')

    return render(request, 'pasta_form.html')

@login_required(login_url='login')
def editarPasta(request, pk):
    page = 'editing'
    pasta = get_object_or_404(Pasta, id=pk)

    if request.user != pasta.user:
        return HttpResponse('Você não tem acesso à essa página!')
    
    if request.method == "POST":
        is_private = request.POST.get('visibilidade') == 'privado' #retorna true(privado) ou false(publico)
        pasta.titulo = request.POST.get('titulo')
        pasta.descricao = request.POST.get('descricao')
        pasta.is_private = is_private

        if 'capa' in request.FILES:
            pasta.capa = request.FILES.get('capa')
        else:
            pasta.capa = pasta.capa or 'capas_pastas/default.png'

        pasta.save() 
        return redirect('pastas')

    context = {
        'page': page,
        'pasta': pasta,
    }
    return render(request, 'pasta_form.html', context)

@login_required(login_url='login')
def deletePasta(request, pk):
    pasta = Pasta.objects.get(id = pk)
    if request.method == 'POST':
        pasta.delete()
        return redirect('home')
    return render(request, 'delete.html', {'obj':pasta})

@login_required(login_url='login')
def pasta(request, pk):
    pasta = Pasta.objects.get(id = pk)
    livros = Pasta_livro.objects.filter(pasta=pasta).select_related('livro')

    context = {
        'pasta': pasta,
        'livros': livros,
    }
    return render(request, 'pasta.html', context)

