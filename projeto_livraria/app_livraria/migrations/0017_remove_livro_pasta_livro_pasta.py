# Generated by Django 5.1.3 on 2024-12-07 17:52

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_livraria', '0016_livro_pasta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='livro',
            name='pasta',
        ),
        migrations.AddField(
            model_name='livro',
            name='pasta',
            field=models.ManyToManyField(to='app_livraria.pasta'),
        ),
    ]