# Generated by Django 5.1.3 on 2024-12-08 11:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app_livraria', '0017_remove_livro_pasta_livro_pasta'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='profile',
            name='email',
        ),
        migrations.AddField(
            model_name='profile',
            name='is_private',
            field=models.BooleanField(default=True),
        ),
    ]
