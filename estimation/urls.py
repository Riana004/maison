from django.urls import path
from . import views

urlpatterns = [
    path('location/', views.location, name='location'),
    path('achat/', views.achat, name='achat'),
    path('ville/', views.ville, name='ville'),
    path('', views.accueil, name='accueil'),
    path('train_maison/', views.train_maison_model, name='train_maison'),
    path('train_terrain/', views.train_terrain_model, name='train_terrain'),
]