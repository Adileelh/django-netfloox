
import json
from django.http import JsonResponse, HttpResponse
from render_block import render_block_to_string
import joblib
from sklearn.metrics.pairwise import cosine_similarity
from django.shortcuts import render
from django.views.decorators.cache import cache_page
import pandas as pd
from .models import Films
from sklearn.feature_extraction.text import TfidfVectorizer


"""
fonction qui affiche la page d'accueil
"""


def index(request):
    return render(request, "index/index.html")


def test(request):
    return render(request, "index/test.html")


@cache_page(60)
def search_films(request):
    limit = 9
    query = request.GET.get('query')
    if query:
        films = Films.objects.filter(originaltitle__icontains=query)[:limit]
    else:
        films = Films.objects.all()

    context = {'films': films}
    html = render_block_to_string('index/index.html', 'show-film', context)
    return HttpResponse(html)


def get_film_index(request):
    # Charger la matrice
    count_matrix_svd_norm = joblib.load("static/data/model.pkl")

    if request.method == 'GET':
        film_name = request.GET.get('film_name')

        if not film_name:
            # Renvoyer une réponse vide si film_name n'est pas fourni
            return HttpResponse('')

        # Charger les données des films
        df = pd.read_csv('static/data/similarity.csv', low_memory=False)
        idx = df[df['originalTitle'] == film_name].index[0]

        # Trouver la similarité cosinus entre le film recherché et les autres films
        cosine_sim = cosine_similarity(
            [count_matrix_svd_norm[idx]], count_matrix_svd_norm)

        # Retourner les titres des films correspondant aux scores de similarité les plus élevés
        similar_movies = []
        for i in cosine_sim[0].argsort()[:-6:-1]:
            if i != idx:
                similar_movies.append(df['originalTitle'][i])

        return JsonResponse({'similar_movies': similar_movies})


def predict_rating(request):
    if request.method == 'POST':
        genres = request.POST.get('genres')
        actor = request.POST.get('actor')
        director = request.POST.get('director')
        producer = request.POST.get('producer')
        writer = request.POST.get('writer')
        actress = request.POST.get('actress')

        # Check if any of the input fields are empty
        if not all([genres, actor, director, producer, writer, actress]):
            context = {
                'error': 'Please fill in all fields'
            }
            return render(request, 'index/index.html', context)

        # Chargement du modèle
        model = joblib.load('static/data/pop2.pkl')

        # Préparation des données
        data = [genres + " " + actor + " " + director +
                " " + producer + " " + writer + " " + actress]

        # Prédiction
        x = TfidfVectorizer().fit_transform(data).toarray()

        y_pred = model.predict(x.tolist())[0]

        # Affichage des résultats
        context = {
            'rating': y_pred
        }
        return render(request, 'index/result.html', context)
    else:
        context = {}
        return render(request, 'index/index.html', context)


"""
def get_film_indexe(request):
    # Charger la matrice
    count_matrix_svd_norm = joblib.load("static/data/model.pkl")

    film_name = request.POST.get('film_name')
    # Ajouter une vérification pour s'assurer que le nom du film a été correctement envoyé
    if not film_name:
        return JsonResponse({'error': 'Le nom du film est manquant.'})

    # Charger les données des films
    df = pd.read_csv('static/data/similarity.csv', low_memory=False)
    idx = df[df['originalTitle'] == film_name].index[0]

    # Trouver la similarité cosinus entre le film recherché et les autres films
    cosine_sim = cosine_similarity(
        [count_matrix_svd_norm[idx]], count_matrix_svd_norm)

    # Retourner les titres des films correspondant aux scores de similarité les plus élevés
    similar_movies = []
    for i in cosine_sim[0].argsort()[:-6:-1]:
        if i != idx:
            similar_movies.append(df['originalTitle'][i])

    # Renvoyer le nom du film en tant que réponse JSON
    return JsonResponse({'film_name': film_name, 'similar_movies': similar_movies})


def my_view(request):
    value = request.GET.get('my-paragraph')
    return render(request, 'my_template.html', {'value': value})

def get_film_index(request):
    # Charger la matrice
    count_matrix_svd_norm = joblib.load("static/data/model.pkl")

    film_name = request.GET.get('value')

    # Charger les données des films
    df = pd.read_csv('static/data/similarity.csv', low_memory=False)
    idx = df[df['originalTitle'] == film_name].index[0]

    # Trouver la similarité cosinus entre le film recherché et les autres films
    cosine_sim = cosine_similarity(
        [count_matrix_svd_norm[idx]], count_matrix_svd_norm)

    # Retourner les titres des films correspondant aux scores de similarité les plus élevés
    similar_movies = []
    for i in cosine_sim[0].argsort()[:-6:-1]:
        if i != idx:
            similar_movies.append(df['originalTitle'][i])

    context = {'similar_movies': similar_movies}

    return render(request, 'partials/movie-film.html', context)
def get_film_index(request):
    # Charger la matrice
    count_matrix_svd_norm = joblib.load("static/data/model.pkl")

    film_name = request.GET.get('value')
    # Charger les données des films
    df = pd.read_csv('static/data/similarity.csv', low_memory=False)
    idx = df[df['originalTitle'] == film_name].index[0]

    # Trouver la similarité cosinus entre le film recherché et les autres films
    cosine_sim = cosine_similarity(
        [count_matrix_svd_norm[idx]], count_matrix_svd_norm)

    # Retourner les titres des films correspondant aux scores de similarité les plus élevés
    similar_movies = []
    for i in cosine_sim[0].argsort()[:-6:-1]:
        if i != idx:
            similar_movies.append(df['originalTitle'][i])

    context = {'similar_movies': similar_movies}

    return JsonResponse(context)
def get_film_index(request):
    # Charger la matrice
    count_matrix_svd_norm = joblib.load("data/model.pkl")

    film_name = request.GET.get('value')
    # Charger les données des films
    df = pd.read_csv('static/data/similarity.csv', low_memory=False)
    idx = df[df['originalTitle'] == film_name].index[0]

    # Trouver la similarité cosinus entre le film recherché et les autres films
    cosine_sim = cosine_similarity(
        [count_matrix_svd_norm[idx]], count_matrix_svd_norm)

    # Retourner les titres des films correspondant aux scores de similarité les plus élevés
    similar_movies = []
    for i in cosine_sim[0].argsort()[:-6:-1]:
        if i != idx:
            similar_movies.append(df['originalTitle'][i])

    for movie in similar_movies:
        return movie

    context = {'movies': movie}

    return render(request, 'partials/list-film.html', context)
def search_films(request):
    query = request.GET.get('query')
    if query:
        df = pd.read_csv('static/data/similarity.csv')
        results = df[df['originalTitle'].str.contains(query)]
        films = results['originalTitle'].tolist()
    else:
        films = []

    context = {'films': films}
    return render(request, 'partials/list-film.html', context)


"""
