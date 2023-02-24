from core.models import Films

import csv


def run():
    with open('static/data/similarity.csv') as file:
        reader = csv.reader(file)
        next(reader)  # Advance past the header

        Films.objects.all().delete()

        for line in reader:

            films = Films(
                tconst=line[0],
                originaltitle=line[1],
                runtimeminutes=line[2] if line[2] else None,
                averagerating=line[3] if line[3] else None,
                numvotes=line[4],
                movie_features=line[5],
            )
            films.save()
