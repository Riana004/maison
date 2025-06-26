from django import forms
import joblib
import pandas as pd
from sklearn.preprocessing import MultiLabelBinarizer
from .models import Maison, Terrain, Accessibilite, Type, Type_papier, Commodite
import numpy as np
from django.utils.translation import gettext_lazy as _

from django import forms

class VilleForm(forms.Form):
    ville_nom = forms.CharField(
        label=_("Ville sélectionnée"),
        widget=forms.TextInput(attrs={
            'class': 'form-control mt-3',
            'readonly': True,
            'placeholder': _('Cliquez sur la carte pour sélectionner...')
        })
    )
    latitude = forms.FloatField(widget=forms.HiddenInput())
    longitude = forms.FloatField(widget=forms.HiddenInput())

from django.utils.translation import gettext_lazy as _

class MaisonForm(forms.ModelForm):
    accessibilite = forms.ModelChoiceField(
        queryset=Accessibilite.objects.all(),
        label=_("Type d'accès"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        label=_("Type de logement"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    commodite = forms.ModelMultipleChoiceField(
        queryset=Commodite.objects.all(),
        label=_("Commodités"),
        widget=forms.CheckboxSelectMultiple
    )
    nb_chambres = forms.IntegerField(
        label=_("Nombre de chambres"),
        widget=forms.NumberInput(attrs={
            'class': 'form-control',
        })
    )

    class Meta:
        model = Maison
        fields = ['ville', 'accessibilite', 'type', 'commodite', 'nb_chambres']
        widgets = {
            'ville': forms.TextInput(
                attrs={
                    'class': 'form-control mt-3',
                    'readonly': True,
                    'placeholder': _('Cliquez sur la carte pour sélectionner...')
                }),
        }

    def predict_price(self):
        # Charger le modèle une seule fois (à mettre en variable de classe si possible)
        model = joblib.load('estimation/ml_model/estimation_maison_model.joblib')
        mlb = MultiLabelBinarizer()

        # Préparer les données
        input_data = {
            'ville': [self.cleaned_data['ville']],
            'accessibilite': [self.cleaned_data['accessibilite'].nom],
            'type': [self.cleaned_data['type'].nom],
            'type_logement': [self.cleaned_data['type'].logement],
            'nb_chambres': [int(self.cleaned_data['nb_chambres'])]
        }

        # Prédiction
        df = pd.DataFrame(input_data)

        commodites_list = [c.nom for c in self.cleaned_data['commodite']]

        # Encoder les commodités
        commodites_encoded = mlb.fit_transform([commodites_list])
        commodites_df = pd.DataFrame(commodites_encoded, columns=mlb.classes_)

        # Fusionner avec le DataFrame principal
        df = pd.concat([df, commodites_df], axis=1)

        # S'assurer que les colonnes sont dans le même ordre que lors de l'entraînement
        df = df.reindex(columns=model.feature_names_in_, fill_value=0)

        predicted_price = model.predict(df)[0]
        return round(float(predicted_price), 2)  # Correction ici (point au lieu de virgule)

class TerrainForm(forms.ModelForm):
    accessibilite = forms.ModelChoiceField(
        queryset=Accessibilite.objects.all(),
        label= _("Type d'accès"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    type_papier = forms.ModelChoiceField(
        queryset=Type_papier.objects.all(),
        label= _("Type de papier"),
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    class Meta:
        model = Terrain
        fields = ['ville', 'type_papier','accessibilite', 'est_cloture', 'est_pret_a_construire']
        widgets = {
            'ville': forms.TextInput(attrs={
                    'class': 'form-control mt-3',
                    'readonly': True,
                    'placeholder': _('Cliquez sur la carte pour sélectionner...')
                }),
            'est_cloture': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'est_pret_a_construire': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
        }
        labels = {
            'est_cloture': _('Terrain clôturé'),
            'est_pret_a_construire': _('Prêt à construire')
        }
    def predict_price(self):
        # Charger le modèle
        model = joblib.load('estimation/ml_model/estimation_terrain_model.joblib')

        # Préparer les données
        input_data = {
            'ville': [self.cleaned_data['ville']],
            'type_papier__nom': [self.cleaned_data['type_papier'].nom],
            'accessibilite__nom': [self.cleaned_data['accessibilite'].nom],
            'est_cloture': [bool(self.cleaned_data['est_cloture'])],
            'est_pret_a_construire': [bool(self.cleaned_data['est_pret_a_construire'])]
        }

        # Prédiction
        df = pd.DataFrame(input_data)
        predicted_price = model.predict(df)[0]
        return round(float(predicted_price), 2)  # Correction ici