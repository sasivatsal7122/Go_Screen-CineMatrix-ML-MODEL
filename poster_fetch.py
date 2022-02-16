import pandas as pd
import requests
import difflib


mymdf = pd.read_csv("Datasets/moviesss.csv")
tmdb = pd.read_csv("Datasets/tmdb_5000_movies.csv")

def movie_poster_fetch(movie_ls):

    titles=[]
    for movie in movie_ls:
        close_match = difflib.get_close_matches(movie, list(tmdb['title']))
        if bool(close_match):
            titles.append(close_match[0])
    print(titles)  


    movie_id_ls=[]
    for title in titles:
        x = tmdb.loc[tmdb['original_title'] == title]
        if x.size!=0:
            movie_id = x['id'].values[0]
            movie_id_ls.append(movie_id)
    print(movie_id_ls)

    def fetch_poster(movie_id):
        url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
        data = requests.get(url)
        data = data.json()
        poster_path = data['poster_path']
        full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
        print(full_path)
        
    for m_id in movie_id_ls:
        (fetch_poster(m_id))