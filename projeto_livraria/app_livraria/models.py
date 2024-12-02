from django.db import models

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    genero = models.CharField(max_length=200)
    sinopse = models.TextField(max_length=4000)
    capa = models.ImageField(upload_to='capas_livros/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo
