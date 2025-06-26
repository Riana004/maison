import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'maison.settings')
django.setup()

from estimation.models import Terrain
import joblib
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import OneHotEncoder
from sklearn.compose import ColumnTransformer
from sklearn.pipeline import Pipeline

# Query all Terrain objects and convert to DataFrame
terrains = Terrain.objects.all().values(
    'ville', 'prix', 'type_papier__nom', 
    'accessibilite__nom', 'est_cloture', 'est_pret_a_construire'
)
df = pd.DataFrame(terrains)

# Assume 'prix' is the target variable
X = df.drop('prix', axis=1)
y = df['prix']

# Identify categorical columns
categorical_cols = X.select_dtypes(include=['object', 'category']).columns.tolist()
numerical_cols = X.select_dtypes(include=['number']).columns.tolist()

# Preprocessing for categorical data
preprocessor = ColumnTransformer(
    transformers=[
        ('cat', OneHotEncoder(handle_unknown='ignore'), categorical_cols)
    ],
    remainder='passthrough'
)

# Pipeline: preprocessing + regression
model = Pipeline(steps=[
    ('preprocessor', preprocessor),
    ('regressor', LinearRegression())
])

# Split data
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Train model
model.fit(X_train, y_train)

print("Modèle Terrain entraîné.")
    
# Enregistrement du modèle
joblib.dump(model, 'estimation/ml_model/estimation_terrain_model.joblib')