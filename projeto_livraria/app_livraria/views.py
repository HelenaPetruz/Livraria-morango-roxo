from django.shortcuts import render
from django.db.models import Q
from .models import Livro, Autor, Autor_livro, Comentario, Genero_literario



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