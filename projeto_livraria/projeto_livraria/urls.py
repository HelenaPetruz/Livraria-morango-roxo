from django.contrib import admin
from django.urls import path
from app_livraria import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('login/', views.loginPage, name="login"),
    path('logout/', views.logoutUser, name="logout"),
    path('register/', views.registerPage, name="register"),
    path('perfil/<int:pk>', views.userPerfil, name="user-perfil"),
    path('criar-perfil', views.criarPerfil, name="criar-perfil"),
    path('editar-perfil', views.updateUser, name="editar-perfil"),

    path('admin/', admin.site.urls),
    #link inicial:
    path('', views.home, name='home'),
    path('livro/<int:pk>/', views.livro, name='livro'),
    path('adicionar-livros/<int:pk>', views.adicionarLivro, name="adicionar-livros"),

    path('pastas/', views.pastas, name="pastas"),
    path('criar-pasta/', views.criarPasta, name="criar-pasta"),
    path('editar-pasta/<str:pk>', views.editarPasta, name="editar-pasta"),
    path('delete-pasta/<str:pk>', views.deletePasta, name="delete-pasta"),
    

    path('pasta/<int:pk>/', views.pasta, name='pasta'),

    path('delete-comentario/<str:pk>', views.deleteComentario, name="delete-comentario"),
    path('editar-comentario/<int:comentario_id>/', views.editarComentario, name="editar-comentario"),

    path('comando/', views.comando, name="comando")
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
