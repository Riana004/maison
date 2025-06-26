import os
import django
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder, MultiLabelBinarizer
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Initialisation Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maison.settings')
django.setup()

from estimation.models import Maison

# Récupérer les données Maison
maisons = Maison.objects.all()

data = []
for maison in maisons:
    commodites = list(maison.commodite.values_list('nom', flat=True)) 
    maison_dict = {
        'ville': maison.ville,
        'prix': maison.prix,
        'accessibilite': maison.accessibilite.nom,
        'type': maison.type.nom,
        'type_logement': maison.type.logement,
        'nb_chambres': maison.nb_chambres,
        'commodites': commodites
    }
    data.append(maison_dict)

df_maison = pd.DataFrame(data)

mlb = MultiLabelBinarizer()
commodites_encoded = mlb.fit_transform(df_maison['commodites'])
commodites_df = pd.DataFrame(commodites_encoded, columns=mlb.classes_)

# Fusionner avec le DataFrame d'origine (en supprimant la colonne 'commodites')
df_maison = pd.concat([df_maison.drop('commodites', axis=1), commodites_df], axis=1)

# Pour chaque modèle, on suppose qu'il y a une colonne 'prix' à prédire
X_maison = df_maison.drop('prix', axis=1)
y_maison = df_maison['prix']
cat_cols_maison = X_maison.select_dtypes(include=['object', 'category']).columns.tolist()

preprocessor_maison = ColumnTransformer(
    transformers=[('cat', OneHotEncoder(handle_unknown='ignore'), cat_cols_maison)],
    remainder='passthrough'
)
model_maison = Pipeline([
    ('preprocessor', preprocessor_maison),
    ('regressor', LinearRegression())
])
X_train, X_test, y_train, y_test = train_test_split(X_maison, y_maison, test_size=0.2, random_state=42)
model_maison.fit(X_train, y_train)

print("Modèle Maison entraîné.")
joblib.dump(model_maison, 'estimation/ml_model/estimation_maison_model.joblib')