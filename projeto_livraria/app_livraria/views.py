from django.shortcuts import render
from .models import Livro, Autor, Autor_livro

livros = {
        'livros': Livro.objects.all()
    }

def home(request):
    return render(request,'home.html', livros)

def livro(request, pk):
    livros = Livro.objects.all()
    livro = None
    for i in livros:
        if i.id == int(pk):
            livro = i
            break

    autores_livros = Autor_livro.objects.all()
    for a in autores_livros:
        if a.livro == livro:
            autor = a.autor
            break

    context = {
        'livro': livro,
        'autor': autor
    }
    return render(request, 'livro.html', context)