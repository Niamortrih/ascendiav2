import os
import numpy as np
from sklearn.ensemble import HistGradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import StandardScaler
import joblib

# Spécifier le dossier contenant les fichiers .npz
dataset_folder = "datasets"

# Liste des fichiers .npz dans le dossier
dataset_files = [os.path.join(dataset_folder, f) for f in os.listdir(dataset_folder) if f.endswith(".npz")]

# Initialisation des listes pour stocker les données cumulées
X_list = []
y_list = []
names_list = []

# Chargement et concaténation
for file in dataset_files:
    data = np.load(file)
    X_list.append(data["X"])
    y_list.append(data["y"].astype(np.float32))
    names_list.append(data["names"])

# Concaténation finale en un seul tableau
X = np.concatenate(X_list, axis=0)
y = np.concatenate(y_list, axis=0)
names = np.concatenate(names_list, axis=0)

print(f"X shape: {X.shape}, y shape: {y.shape}, names shape: {names.shape}")

n_total = len(X)
n_test = int(n_total * 0.2)
n_train = n_total - n_test

# Split manuel : 80 % pour l'entraînement, 20 % pour le test
X_train, X_test = X[:n_train], X[n_train:]
y_train, y_test = y[:n_train], y[n_train:]
names_train, names_test = names[:n_train], names[n_train:]

# Standardisation
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# Entraînement du modèle
model = HistGradientBoostingRegressor(
    max_iter=8000,
    random_state=42,
    verbose=1,
)
model.fit(X_train_scaled, y_train)

# Prédiction
y_pred = model.predict(X_test_scaled)

# Évaluation
rmse = mean_squared_error(y_test, y_pred, squared=False)
print("RMSE:", rmse)

# Calcul des erreurs et tri par erreur décroissante
results = []
for i in range(len(y_test)):
    yt = y_test[i]
    yp = y_pred[i]
    err = abs(yt - yp)
    name = names_test[i]
    results.append((err, i, name, yt, yp))

results.sort(reverse=True)

# Affichage trié (Top 50 avec inputs)
print("\n Prédictions triées par erreur décroissante (top 50) :\n")
for rank, (err, i, name, yt, yp) in enumerate(results[:50], 1):
    inputs = X_test[i]
    print(f"{rank:3} | Board : {name} | EV Réelle : {yt*100:.2f} %Pot | Prédiction IA : {yp*100:.2f} %Pot | Erreur : {err*100:.2f} %Pot")
    print(f"      Inputs : {[round(v, 2) for v in inputs]}")

# Moyenne d'erreur absolue
mean_error = np.mean(np.abs(y_test - y_pred))
print(f"\nMoyenne d’erreur absolue : {mean_error*100:.3f} %Pot")

# Sauvegarde du modèle
joblib.dump(model, "model.pkl")
joblib.dump(scaler, "scaler.pkl")
