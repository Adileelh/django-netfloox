function getSimilarMovies() {
    // Récupérer la valeur du paragraphe
    var filmName = document.getElementById("input").value;

    // Encoder la valeur du film
    var encodedFilmName = encodeURIComponent(filmName);

    // Envoyer la requête GET avec la valeur encodée
    var xhr = new XMLHttpRequest();
    xhr.open("GET", "/get_film_index/?film_name=" + encodedFilmName);
    xhr.onload = function() {
        if (xhr.status === 200) {
            var response = JSON.parse(xhr.responseText);
            var similarMovies = response.similar_movies;
            var moviesList = document.getElementById("similar-movies");
            moviesList.innerHTML = "";
            for (var i = 0; i < similarMovies.length; i++) {
                var movie = similarMovies[i];
                var listItem = document.createElement("li");
                listItem.textContent = movie;
                moviesList.appendChild(listItem);
            }
        }
    };
    xhr.send();
}




function selectResult(element) {
    const input = document.getElementById('input');
    input.value = element.textContent.trim();
    const resultsDiv = document.getElementById('results');
    resultsDiv.style.display = 'none';
  }

