# Les imports
from sklearn.neighbors import NearestNeighbors
from sqlalchemy.sql import text
import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sqlalchemy import create_engine, types
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from sklearn.preprocessing import StandardScaler
from scipy.sparse import csr_matrix
import os
import yaml  # credentials:

# Récup des info de connection
with open('config.yaml', 'r') as file:
    config = yaml.safe_load(file)
# print(config)

cfg = config['mysql']
print(cfg)
# Connection à BDD
url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
print('URL', url)
engine = create_engine(url)


sql = ''' SELECT B.tconst, titleType, originalTitle, runtimeMinutes, genres, averageRating, numVotes, P.nconst, category, primaryName
                FROM title_basics as B
                INNER JOIN title_ratings as R
                on B.tconst = R.tconst
                INNER JOIN title_principals as P
                on B.tconst = P.tconst
                INNER JOIN name_basics as N 
                on N.nconst = P.nconst             
                WHERE titleType = "movie" 
                AND (P.category = 'director' OR P.category = 'actor' OR P.category = 'actress' OR P.category = 'producer' OR P.category = 'writer')
                
                ;'''


with engine.connect().execution_options(autocommit=True) as conn:
    query = conn.execute(text(sql))
df6 = pd.DataFrame(query.fetchall())


def get_first_genre(x):
    if x is not None and len(x) > 0:
        return x.split(',')[0]
    else:
        return ''


df6['genres'] = df6['genres'].apply(get_first_genre)

# print(df6)
df_first = df6[['tconst', 'originalTitle', 'runtimeMinutes',
                'genres', 'averageRating', 'numVotes']].drop_duplicates()

# Regrouper les données par tconst et category, et extraire les trois premiers noms de chaque catégorie
grouped = df6.groupby(['tconst', 'category'])[
    'primaryName'].apply(lambda x: ', '.join(x[:3]))
# print(grouped)
# Pivoter les données pour obtenir une table avec une colonne pour chaque catégorie
data_pivoted = grouped.unstack()
# print(data_pivoted)
# Réinitialiser l'index pour en faire une colonne
data_pivoted = data_pivoted.reset_index()
# print(data_pivoted)

df = pd.merge(df_first, data_pivoted, on='tconst')

df = df.to_csv('data/similarity_0.csv', index=False)


# def concat_features(row):
#   return (str(row['genres']).replace(",", " ") + " " + str(row['director']).replace(" ", "").replace(",", "") + " " + str(row["actor"]).replace(" ", "").replace(",", "") + " " + str(row["actress"]).replace(" ", "").replace(",", "") + " " + str(row["producer"]).replace(" ", "").replace(",", " ") + " " + str(row["writer"]).replace(" ", "").replace(",", " "))


# df["movie_features"] = df.apply(concat_features, axis=1)
# print(df)

# df = df.drop(['genres', 'director', "actor",
#             "actress", "producer", "writer"], axis=1)
# print(df)
# df = df.to_csv('data/similarity.csv', index=False)


# creer des class pour les valeurs numeric
# y target X differentes features
# encode genre, acteur, ...
# donnee numerique

# hyperparametre
