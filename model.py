

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
# print(cfg)
# Connection à BDD
url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
# print('URL', url)
engine = create_engine(url)


sql = ''' SELECT B.tconst, titleType, runtimeMinutes, genres, averageRating, numVotes, P.nconst, category, primaryName
                FROM title_basics as B
                INNER JOIN title_ratings as R
                on B.tconst = R.tconst
                INNER JOIN title_principals as P
                on B.tconst = P.tconst
                INNER JOIN name_basics as N
                on N.nconst = P.nconst
                WHERE titleType = "movie"
                AND (P.category = 'director' OR P.category = 'actor' OR P.category = 'actress' OR P.category = 'producer' OR P.category = 'writer')
                AND numVotes > 0
                AND numVotes IS NOT NULL
                AND averageRating > 0
                AND averageRating IS NOT NULL


                ;'''


with engine.connect().execution_options(autocommit=True) as conn:
    query = conn.execute(text(sql))
df_full = pd.DataFrame(query.fetchall())


def get_first_genre(x):
    if x is not None and len(x) > 0:
        return x.split(',')[0]
    else:
        return ''


df_full['genres'] = df_full['genres'].apply(get_first_genre)


df_first = df_full[['tconst', 'runtimeMinutes',
                    'genres', 'averageRating', 'numVotes']].drop_duplicates()
# print(df_full)
df_second = df_full.groupby(['tconst', 'category'])[
    'primaryName'].apply(lambda x: ', '.join(x.iloc[:1]))

# print(df_second)

# Pivoter les données pour obtenir une table avec une colonne pour chaque catégorie et reinitialiser l'index
data_second_pivoted = df_second.unstack().reset_index()
# print(data_pivoted)

df = pd.merge(df_first, data_second_pivoted, on='tconst')


# df = df.to_csv('data/regressionData.csv', index=False)


df = df.dropna()
print(df)

# df = df.to_csv('data/data.csv', index=False)
