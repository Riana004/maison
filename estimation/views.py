
from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import MaisonForm, TerrainForm, VilleForm
import subprocess

def ville(request):
    if request.method == 'POST':
        form = VilleForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('confirmation.html')
    else:
        form = VilleForm()
    
    return render(request, 'template.html', {'form': form})

def location(request):
    if request.method == 'POST':
        form = MaisonForm(request.POST)
        if form.is_valid():
            maison = form.save(commit=False)
            
            # Prédiction du prix
            try:
                prix_estime = form.predict_price()
                maison.prix = prix_estime  # Assigner le prix prédit
                
                # Préparation des données pour le template
                context = {
                    'prix_estime': prix_estime,
                    'maison': maison,
                    'form': form
                }
                return render(request, 'confirmation_maison.html', context)
                
            except Exception as e:
                messages.error(request, f"Erreur lors de l'estimation: {str(e)}")
                return render(request, 'template.html', {'form': form})
    else:
        form = MaisonForm()
    
    return render(request, 'template.html', {'form': form})

def achat(request):
    if request.method == 'POST':
        form = TerrainForm(request.POST)
        if form.is_valid():
            terrain = form.save(commit=False)
            
            # Prédiction du prix
            try:
                prix_estime = form.predict_price()
                terrain.prix = prix_estime 
                context = {
                    'prix_estime': prix_estime,
                    'terrain': terrain,
                    'form': form
                }
                return render(request, 'confirmation_terrain.html', context)
                
            except Exception as e:
                messages.error(request, f"Erreur lors de l'estimation: {str(e)}")
                return render(request, 'template.html', {'form': form})
    else:
        form = TerrainForm()
    
    return render(request, 'template.html', {'form': form})

def accueil(request):
    return render(request, 'index.html')

def train_maison_model(request):
    try:
        # Entraînement du modèle de prédiction pour les maisons
        result = subprocess.run(['python', 'maison_train.py'], check=True, capture_output=True, text=True)
        messages.success(request, "Modèle de maison entraîné avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'entraînement du modèle: {str(e)}")
    
    return redirect('accueil')

def train_terrain_model(request):
    try:
        # Entraînement du modèle de prédiction pour les terrains
        result = subprocess.run(['python', 'terrain_train.py'], check=True, capture_output=True, text=True)
        messages.success(request, "Modèle de terrain entraîné avec succès.")
    except Exception as e:
        messages.error(request, f"Erreur lors de l'entraînement du modèle: {str(e)}")
    
    return redirect('accueil')