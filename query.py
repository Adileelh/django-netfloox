import joblib
import pandas as pd
from sklearn.metrics.pairwise import cosine_similarity

# Charger les données des films
df = pd.read_csv("data/similarity.csv", low_memory=False)

# Charger la matrice
count_matrix_svd_norm = joblib.load("data/model.pkl")

# Demander à l'utilisateur d'entrer un titre de film
query = input("Entrez le titre d'un film: ")

# Trouver l'indice correspondant à ce titre de film
idx = df[df['originalTitle'] == query].index[0]

# Trouver la similarité cosinus entre le film recherché et les autres films
cosine_sim = cosine_similarity(
    [count_matrix_svd_norm[idx]], count_matrix_svd_norm)

# Retourner les titres des films correspondant aux scores de similarité les plus élevés
similar_movies = []
for i in cosine_sim[0].argsort()[:-6:-1]:
    if i != idx:
        similar_movies.append(df['originalTitle'][i])
print("Les films les plus similaires à", query, "sont:")
for movie in similar_movies:
    print("-", movie)
