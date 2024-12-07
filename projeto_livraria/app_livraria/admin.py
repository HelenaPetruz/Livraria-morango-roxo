from django.contrib import admin
from .models import Livro, Autor, Autor_livro, Genero_literario, Comentario, Genero_livro, Pasta, Pasta_livro, Profile

admin.site.register(Livro)
admin.site.register(Autor)
admin.site.register(Autor_livro)
admin.site.register(Genero_literario)
admin.site.register(Comentario)
admin.site.register(Genero_livro)
admin.site.register(Pasta)
admin.site.register(Pasta_livro)
admin.site.register(Profile)