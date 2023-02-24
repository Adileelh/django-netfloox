"""
import joblib
from sklearn.neighbors import NearestNeighbors
import pandas as pd
import numpy as np
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD


df = pd.read_csv("data/similarity.csv", encoding="ISO-8859-1")


# Créer une matrice de comptage
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['movie_features'])

# Effectuer une décomposition en valeurs singulières tronquée
n_components = 200
svd = TruncatedSVD(n_components=n_components)
count_matrix_svd = svd.fit_transform(count_matrix)

# Normaliser les vecteurs de la matrice SVD
norms = np.apply_along_axis(np.linalg.norm, 1, count_matrix_svd)
count_matrix_svd_norm = count_matrix_svd / norms[:, np.newaxis]

# Créer une matrice de similarité en utilisant cosine_similarity
cosine_sim = cosine_similarity(count_matrix_svd_norm)

# Créer un objet NearestNeighbors
k = 6
nn = NearestNeighbors(n_neighbors=k, metric='euclidean')

# Ajuster l'objet NearestNeighbors à votre matrice de similarité
nn.fit(count_matrix_svd_norm)


# sauvegarder le modèle entraîné dans un fichier
filename = 'data/knn_model.sav'
joblib.dump(nn, filename)
"""


import pandas as pd
import joblib
import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.decomposition import TruncatedSVD
from sklearn.preprocessing import normalize

# Charger les données des films
df = pd.read_csv("data/similarity.csv", low_memory=False)


# Créer une matrice de similarité en utilisant CountVectorizer et cosine_similarity
cv = CountVectorizer()
count_matrix = cv.fit_transform(df['movie_features'])
count_matrix = count_matrix.astype('float32')

# Réduire la dimension de la matrice en utilisant TruncatedSVD
svd = TruncatedSVD(n_components=200)
count_matrix_svd = svd.fit_transform(count_matrix)
count_matrix_svd_norm = normalize(count_matrix_svd, norm='l2', axis=1)

# joblib.dump(count_matrix_svd_norm, 'data/model.pkl')
print(count_matrix[0])
print("#################################")
print(count_matrix_svd[0])
print("#################################")
print(count_matrix_svd_norm[0])
