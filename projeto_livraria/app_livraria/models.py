from django.db import models
from django.contrib.auth.models import User

class Genero_literario(models.Model):
    nome = models.CharField(max_length=200)

    def __str__(self):
        return self.nome
    

class Livro(models.Model):
    titulo = models.CharField(max_length=200)
    sinopse = models.TextField(max_length=4000)
    capa = models.ImageField(upload_to='capas_livros/', null=True, blank=True)
    
    def __str__(self):
        return self.titulo

class Genero_livro (models.Model):
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='generos')
    genero = models.ForeignKey(Genero_literario, on_delete=models.CASCADE, related_name='livros')

class Autor(models.Model):
    nome = models.CharField(max_length=200)
    descricao = models.TextField(max_length=4000)
    foto = models.ImageField(upload_to='foto/', null=True, blank=True)

    def __str__(self):
        return self.nome

class Autor_livro(models.Model):
    autor = models.ForeignKey(Autor, on_delete=models.CASCADE, related_name='livros')
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE, related_name='autores')

    class Meta:
        db_table = 'autor_livro'
        unique_together = ('autor', 'livro')

class Comentario(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    livro = models.ForeignKey(Livro, on_delete=models.CASCADE)
    mensagem = models.TextField()
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.mensagem[0:50]
    
class Pasta(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    titulo = models.CharField(max_length=200, null=True, blank=True)
    descricao = models.TextField(max_length=3000, null=True, blank=True)
    capa = models.ImageField(upload_to='capas_pastas/', null=True, blank=True, default='capas_pastas/default.png')
    is_private = models.BooleanField(default=True)
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.titulo
    