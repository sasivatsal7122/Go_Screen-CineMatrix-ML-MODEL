''' A COLLABRATIVE FILTERING MODEL BASED ON TfidfVectorizer,TruncatedSVD,cosine_similarity'''
''' MORE ACCURATE THEN THE V-1 COLLABRATIVE MODEL'''


import numpy as np
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.decomposition import TruncatedSVD
from sklearn.metrics.pairwise import cosine_similarity
import difflib
import poster_fetch
from poster_fetch import *

# reading from the pre-processed dataset
movies=pd.read_csv("moviesss.csv")
ratings=pd.read_csv("Datasets_misc/ratings.csv")
Final = pd.read_csv("Final.csv")


# reading data from the main driver dataset
latent_matrix_1_df = pd.read_csv('latent_matrix_1_df.csv',index_col=0)
latent_matrix_2_df = pd.read_csv('latent_matrix_2_df.csv',index_col=0)


# strictly do not execute this function block , time bokka already anni ready chesi petta
def pre_process():
    
    movies['genres'] = movies['genres'].str.replace('|',' ')
    ratings_f = ratings.groupby('userId').filter(lambda x: len(x) >= 55)
    ratings_f=ratings_f.sample(n=100000,random_state=5)
    movie_list_rating = ratings_f.movieId.unique().tolist()
    movies = movies[movies.movieId.isin(movie_list_rating)]


    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(Final['metadata'])
    tfidf_df = pd.DataFrame(tfidf_matrix.toarray(), index=Final.index.tolist())

    svd = TruncatedSVD(n_components=200)
    latent_matrix = svd.fit_transform(tfidf_df)

    n = 200 
    latent_matrix_1_df = pd.DataFrame(latent_matrix[:,0:n], index=Final.title.tolist())

    ratings_f1 = pd.merge(movies[['movieId']], ratings_f, on="movieId", how="right")
    ratings_f2 = ratings_f1.pivot(index = 'movieId', columns ='userId', values = 'rating').fillna(0)

    svd = TruncatedSVD(n_components=200)
    latent_matrix_2 = svd.fit_transform(ratings_f2)
    latent_matrix_2_df = pd.DataFrame(latent_matrix_2,index=Final.title.tolist())

def recommend(user_fav_movie):
    # take the latent vectors for a selected movie from both content 
    # and collaborative matrixes
    a_1 = np.array(latent_matrix_1_df.loc[user_fav_movie]).reshape(1, -1)
    a_2 = np.array(latent_matrix_2_df.loc[user_fav_movie]).reshape(1, -1)

    # calculating the similartity of this movie with the others in the list
    score_1 = cosine_similarity(latent_matrix_1_df, a_1).reshape(-1)
    score_2 = cosine_similarity(latent_matrix_2_df, a_2).reshape(-1)

    # an average measure of both content and collaborative 
    hybrid = ((score_1 + score_2)/2.0)

    # forming a data frame of similar movies 
    dictDf = {'content': score_1 , 'collaborative': score_2, 'hybrid': hybrid} 
    similar = pd.DataFrame(dictDf, index = latent_matrix_1_df.index )

    # sorting the mmovies according to their similarity
    # one with highest similarity stays on top 
    similar.sort_values('content', ascending=False, inplace=True)
    sim_movie_df = similar[1:].head(10)
    sim_movie_ls = list(sim_movie_df.index.values)
    print("\n====================================================================")   
    print(f"Recommended movies based on the {user_fav_movie} are:") 
    print("====================================================================\n") 
    for movie in sim_movie_ls:
        print(movie)
    return sim_movie_ls


# getting the user input
user_fav_movie = input("enter you're fav movie: ")
# searching for the closest match
close_match = difflib.get_close_matches(user_fav_movie.title(), list(movies['title']))
# seelcting the most closest one
user_fav_movie = close_match[0]
print(user_fav_movie)
# calling the recommender function
movie_ls = recommend(user_fav_movie)
poster_fetch.movie_poster_fetch(movie_ls)
