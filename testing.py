import numpy as np

# Spécifie le chemin du fichier .npz dans le dossier "datasets"
dataset_file = "datasets/dataset__home_romain_solutions_spin_Spins_BvB_GTO_LP_18.npz"  # Remplace ce chemin si nécessaire
# dataset_file = "datasets/dataset1.npz"  # Remplace ce chemin si nécessaire

# Chargement des données depuis le fichier .npz
data = np.load(dataset_file)

# Afficher les noms des clés dans le fichier pour s'assurer que X, y, et names existent
print(f"Clés disponibles dans {dataset_file}: {data.files}")

# Afficher les données pour X, y et names
X = data["X"]
y = data["y"]
names = data["names"]

print(f"X shape: {X.shape}, y shape: {y.shape}, names shape: {names.shape}")
print(f"Exemple de X: {X[:5]}")
print(f"Exemple de y: {y[:5]}")
print(f"Exemple de names: {names[:5]}")
