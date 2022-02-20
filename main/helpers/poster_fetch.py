from email.mime import nonmultipart
import pandas as pd
import requests
import difflib
import pprint

tmdb = pd.read_csv("Datasets/tmdb_5000_movies.csv")

def movie_poster_fetch(movie_ls):

    titles=[]
    for movie in movie_ls:
        close_match = difflib.get_close_matches(movie, list(tmdb['title']))
        if bool(close_match):
            titles.append(close_match[0])
        else:
            titles.append(-1)
    movie_id_ls=[]
    #movie_id_dict = {}
    for title in titles:
        if title!=-1:
            x = tmdb.loc[tmdb['original_title'] == title]
            if x.size!=0:
                movie_id = x['id'].values[0]
                movie_id_ls.append(movie_id)
            else:
                movie_id_ls.append(-1)
        else:
            movie_id_ls.append(-1)
    movie_id_dict = dict(zip(movie_ls, movie_id_ls))
    pprint.pprint(movie_id_dict)
    

    poster_dict={}
    def fetch_poster(movie_id_ls):
        for movie_id in movie_id_ls:
            if movie_id != -1:
                url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
                data = requests.get(url)
                data = data.json()
                poster_path = data['poster_path']
                if poster_path!=None:
                    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
                    poster_dict.update({list(movie_id_dict.keys())[list(movie_id_dict.values()).index(movie_id)]:full_path})
                    print(full_path)
    fetch_poster(movie_id_ls)      
    
