import numpy as np
import joblib
from sklearn.metrics import mean_squared_error

# ----------------------------
# Config
# ----------------------------
dataset_files = [
    "dataset1.npz"  # Tu peux en mettre plusieurs
]
model_file = "model.pkl"
scaler_file = "scaler.pkl"
name_filter = ""  # <- Laisser vide "" pour tout prendre

# ----------------------------
# Chargement du dataset
# ----------------------------
X_list, y_list, names_list = [], [], []
for file in dataset_files:
    data = np.load(file)
    X_list.append(data["X"])
    y_list.append(data["y"].astype(np.float32))
    names_list.append(data["names"])

X = np.concatenate(X_list, axis=0)
y = np.concatenate(y_list, axis=0)
names = np.concatenate(names_list, axis=0)

print(f"Avant filtre : {len(X)} lignes")

# ----------------------------
# Application du filtre sur name
# ----------------------------
if name_filter:
    mask = np.array([name_filter in n for n in names])
    X = X[mask]
    y = y[mask]
    names = names[mask]
    print(f"Après filtre : {len(X)} lignes")

# ----------------------------
# Split train/test identique à l'entraînement
# ----------------------------
n_total = len(X)
n_test = int(n_total * 0.2)
n_train = n_total - n_test

X_train, X_test = X[:n_train], X[n_train:]
y_train, y_test = y[:n_train], y[n_train:]
names_train, names_test = names[:n_train], names[n_train:]

# ----------------------------
# Chargement du modèle et du scaler
# ----------------------------
model = joblib.load(model_file)
scaler = joblib.load(scaler_file)

# ----------------------------
# Transformation des données test
# ----------------------------
X_test_scaled = scaler.transform(X_test)

# ----------------------------
# Prédiction
# ----------------------------
y_pred = model.predict(X_test_scaled)

# ----------------------------
# Évaluation
# ----------------------------
rmse = mean_squared_error(y_test, y_pred, squared=False)
mean_error = np.mean(np.abs(y_test - y_pred))

print(f"RMSE : {rmse:.4f}")
print(f"Moyenne d’erreur absolue : {mean_error*100:.3f} %Pot")

# ----------------------------
# Calcul des erreurs et tri
# ----------------------------
results = []
for i in range(len(y_test)):
    yt = y_test[i]
    yp = y_pred[i]
    err = abs(yt - yp)
    name = names_test[i]
    results.append((err, i, name, yt, yp))

results.sort(reverse=True)

# ----------------------------
# Affichage top 50 erreurs
# ----------------------------
print("\nPrédictions triées par erreur décroissante (top 50) :\n")
for rank, (err, i, name, yt, yp) in enumerate(results[:50], 1):
    inputs = X_test[i]
    print(f"{rank:3} | Board : {name} | EV Réelle : {yt*100:.2f} %Pot | "
          f"Prédiction IA : {yp*100:.2f} %Pot | Erreur : {err*100:.2f} %Pot")
    print(f"      Inputs : {[round(v, 2) for v in inputs]}")
