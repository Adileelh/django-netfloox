from django.urls import path
from core import views

urlpatterns = [
    path('', views.index, name='home'),
    path('test/', views.test, name='test'),
    # path('recherche/', views.recherche, name='recherche'),
    path('search/', views.search_films, name='search_films'),
    path('get_film_index/', views.get_film_index, name='get_film_index'),
    path('predict_rating/', views.predict_rating, name='predict_rating'),
]
