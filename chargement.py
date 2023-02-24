import yaml
import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from urllib import request
import os


def load_and_save_data(list_files, config):

    # Configurer la connexion à la base de données
    cfg = config['mysql']
    url = "{driver}://{user}:{password}@{host}/{database}".format(**cfg)
    engine = create_engine(url)
    print(url)
    print(engine)

    # Lire et traiter les fichiers en utilisant chunksize
#    files = ['title.principals']
    files = ['name.basics', 'title.akas', 'title.basics', 'title.crew',
             'title.episode', 'title.principals', 'title.ratings']
    for fn in files:
        reader = pd.read_csv(f"data/{fn}.tsv.gz",
                             sep="\t",
                             compression="gzip",
                             # chunksize=1000000,
                             low_memory=False,
                             quotechar='',
                             quoting=3,
                             nrows=500000
                             )

        # reader.to_sql(fn.replace('.', '_'), engine, if_exists='replace')

        i = 0

        for chunk in reader:

            if i == 0:
                chunk.to_sql(fn.replace('.', '_'), engine, if_exists='replace')
            else:
                chunk.to_sql(fn.replace('.', '_'), engine, if_exists='append')
            i += 1
            print(chunk)
            print(i)


if __name__ == '__main__':
    # list_files = ['title.principals']
    list_files = ['name.basics.tsv.gz', 'title.akas.tsv.gz', 'title.basics.tsv.gz',
                  'title.crew.tsv.gz', 'title.episode.tsv.gz', 'title.principals.tsv.gz', 'title.ratings.tsv.gz']
    with open('config.yaml', 'r') as file:
        config = yaml.safe_load(file)
    load_and_save_data(list_files, config)
