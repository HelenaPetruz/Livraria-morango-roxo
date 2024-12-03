# Generated by Django 5.1.3 on 2024-12-03 11:26

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_livraria', '0007_alter_livro_genero'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='genero',
        ),
        migrations.CreateModel(
            name='Genero_livro',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('genero', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='livros', to='app_livraria.genero_literario')),
                ('livro', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='generos', to='app_livraria.livro')),
            ],
        ),
    ]
