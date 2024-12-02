from django.contrib import admin
from django.urls import path
from app_livraria import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    #link inicial:
    path('', views.home, name='home'),
    path('livro/<int:pk>/', views.livro, name='livro'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
