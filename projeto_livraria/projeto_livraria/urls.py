from django.contrib import admin
from django.urls import path
from app_livraria import views

urlpatterns = [
    path('admin/', admin.site.urls),
    #link inicial:
    path('', views.home, name='home'),
]
