# Generated by Django 5.1.3 on 2024-12-05 15:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_livraria', '0008_remove_livro_genero_genero_livro'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pasta',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(blank=True, max_length=200, null=True)),
                ('descricao', models.TextField(blank=True, max_length=3000, null=True)),
                ('capa', models.ImageField(blank=True, null=True, upload_to='capas_pastas/')),
            ],
        ),
    ]