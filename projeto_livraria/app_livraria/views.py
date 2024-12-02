from django.shortcuts import render
from .models import Livro, Autor, Autor_livro, Comentario, Genero_literario

livros = {
        'livros': Livro.objects.all()
    }

def home(request):
    return render(request,'home.html', livros)

def livro(request, pk):
    livro = Livro.objects.get(id=pk)

    #autores relacionados ao livro
    autores_livros = Autor_livro.objects.filter(livro=livro).select_related('autor')
    autores = [autor_livro.autor for autor_livro in autores_livros]

    #comentários relacionados ao livro
    comentarios = Comentario.objects.filter(livro=livro)

    context = {
        'livro': livro,
        'autores': autores,
        'comentarios': comentarios,
    }
    return render(request, 'livro.html', context)