''' WRIITEN BY B.SASI VATSAL ON 13-02-2022'''
''' COLLABRATIVE FILTERING BASED ON K-NERAREST NEIGHBOURS ALGORITHM'''

''' importing libraries '''
import pandas as pd
import numpy as np
from scipy.sparse import csr_matrix
from sklearn.neighbors import NearestNeighbors
import difflib

import poster_fetch
from poster_fetch import *

# reading the dataset
df_movies  = pd.read_csv('Datasets_misc/movies.csv')
df_ratings  = pd.read_csv('Datasets_misc/ratings.csv')

def pre_process():
    global movie_user_mat_sparse,movie_to_idx,movie_user_mat
    # counting the no.of ratings per rating i.e 0.5->393068;1.0->776815 etc
    df_ratings_cnt_tmp = pd.DataFrame(df_ratings.groupby('rating').size(), columns=['count'])
    # counting the no.of unique users in the dataset
    num_users = len(df_ratings.userId.unique())
    # counting the no.of unique movies in the dataset 
    num_items = len(df_ratings.movieId.unique())
    # calculating the total count
    total_cnt = num_users * num_items
    rating_zero_cnt = total_cnt - df_ratings.shape[0]
    # creating a df of rating counts combined
    df_ratings_cnt = df_ratings_cnt_tmp.append(pd.DataFrame({'count': rating_zero_cnt}, index=[0.0]),verify_integrity=True,).sort_index()
    # creating a new coloumn and adding a log count 
    df_ratings_cnt['log_count'] = np.log(df_ratings_cnt['count'])
    # getting teh rating frequency, i.e a particular movie got how many ratings.
    # by this we can filter highest popular movie to least poplar movie 
    df_movies_cnt = pd.DataFrame(df_ratings.groupby('movieId').size(), columns=['count'])
    # calculating the quantile deviation 
    df_movies_cnt['count'].quantile(np.arange(1, 0.6, -0.05))

    # filtering the movies based on their popularity
    # setting threshold i.e min limit at 50, anything less thanm 50 will be deeletd from the set
    popularity_thres = 50
    popular_movies = list(set(df_movies_cnt.query('count >= @popularity_thres').index))
    # new df after dropping all teh unpopular movies
    df_ratings_drop_movies = df_ratings[df_ratings.movieId.isin(popular_movies)]

    # counting the no.of ratings given by individual user
    # helpful to find the most active user, by which decison can be taken later
    df_users_cnt = pd.DataFrame(df_ratings_drop_movies.groupby('userId').size(), columns=['count'])
    # caculating the quantile deveitaion for per user ratings count
    df_users_cnt['count'].quantile(np.arange(1, 0.5, -0.05))

    # again filetring tha data by dropping inactive users i.e user with least rating count
    # setting min rating threshold per user as 50, users who rated less than 50 movies will be deleted
    ratings_thres = 50
    # finding the active users i.e users who rated more than 50 movies
    active_users = list(set(df_users_cnt.query('count >= @ratings_thres').index))
    # df after dropping both in active users and un popular movies
    df_ratings_drop_users = df_ratings_drop_movies[df_ratings_drop_movies.userId.isin(active_users)]


    # creating a pivot movie user matrix
    # 1st col contains all the movies id's, followed by nxt cols with userid's
    # for any (x,y) in the matrix contains the rating of that movie given by users
    movie_user_mat = df_ratings_drop_users.pivot(index='movieId', columns='userId', values='rating').fillna(0)
    # creating a dictionary with key as movie title and value as its movie id
    movie_to_idx = {movie: i for i, movie in enumerate(list(df_movies.set_index('movieId').loc[movie_user_mat.index].title))}

    # transforming matrix into scipy sparse matrix using csr_matrix method in scipy library
    # coz our data contains a lot of null values, sparse matrix reduces time complexity
    movie_user_mat_sparse = csr_matrix(movie_user_mat.values)

''' CALLING THE PRE-PROCESS FUNCTION '''
pre_process()

''' Making the model '''
model_knn = NearestNeighbors(metric='cosine', algorithm='brute', n_neighbors=20, n_jobs=-1)
model_knn.fit(movie_user_mat_sparse)


def recommend(model_knn=model_knn,data=movie_user_mat_sparse,fav_movie=" ",mapper=movie_to_idx,n_recommendations=10):
    model_knn.fit(data)
    # getting index of the movie
    idx = movie_to_idx.get(fav_movie)
    distances, indices = model_knn.kneighbors(data[idx], n_neighbors=n_recommendations+1)
    raw_recommends = \
        sorted(list(zip(indices.squeeze().tolist(), distances.squeeze().tolist())), key=lambda x: x[1])[:0:-1]
    # get reverse mapper
    reverse_mapper = {v: k for k, v in mapper.items()}
    movie_ls = []
    print("\n====================================================================")   
    print(f"Recommended movies based on the {fav_movie} using KNN ALGO are:") 
    print("====================================================================\n") 
    for i, (idx, dist) in enumerate(raw_recommends):
        movie_ls.append( reverse_mapper[idx])
        
        ## EXECUTE TO SEE THE DISTANCE , ELSE UNNECSSARY
        #print('{0}: {1}, with distance of {2}'.format(i+1, reverse_mapper[idx], dist))
    
    # PRINTING THE RECOMMENDED MOVIES
    for movie in movie_ls:
        print(movie)
    return movie_ls   
        
user_fav_movie = input("enter you're fav movie: ")
# searching for the closest match
close_match = difflib.get_close_matches(user_fav_movie.title(), list(df_movies['title']))
# seelcting the most closest one
user_fav_movie = close_match[0]
print(user_fav_movie)

''' DRIVER FUNCTION TO MAKE RECOMMENDATIONS '''
movie_ls = recommend(fav_movie=user_fav_movie)
poster_fetch.movie_poster_fetch(movie_ls)
