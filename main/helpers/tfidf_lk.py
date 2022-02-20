# importing libraries
import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import difflib
import poster_fetch
from poster_fetch import *

# reading the data
movies=pd.read_csv("Datasets/tfidf_lk_movies.csv")
movies = movies.sample(50000)


def pre_process(movies):
    # intializing the term frequency inverse document frequency vectorizer class 
    # from sklearn.feature_extraction.text
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform(movies['genres'])
    # linear_kernel is mostly used when there are a Large number of Features in a particular Data
    # and when the data is Linearly separable, that is, it can be separated using a single Line.
    #  Training a SVM with a Linear Kernel is Faster than with any other Kernel.
    global cosine_sim,titles,indices
    # calculating the cosine similarity 
    cosine_sim = linear_kernel(tfidf_matrix, tfidf_matrix)
    titles = movies['title']
    # getting the indices of the all movie titles
    indices = pd.Series(movies.index, index=movies['title'])

def genre_recommendations(indices,title,cosine_sim,titles):
    # index of the user given movie
    idx = indices[title]
    # calculating the similarity score using info from cosine similarity
    sim_scores = list(enumerate(cosine_sim[idx]))
    # sorting them in descending, coz one with highest score is the most similar
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    # taking only the top 5 movies
    sim_scores = sim_scores[1:6]
    # fetching the indices of those top 5 movies
    movie_indices = [i[0] for i in sim_scores]
    # returning thr list of movie titles
    return list(titles.iloc[movie_indices])

def recommend(x):
    pre_process(movies)
    movies_ls = genre_recommendations(indices,x,cosine_sim,titles)
    # printing the movies
    print("\n====================================================================")   
    print("Recommended movies based on the genre(tfidf_lk) are:") 
    print("====================================================================\n") 
    for mov in movies_ls:
        print(mov)
    return movies_ls
   
def tfidf_lk_recommend(user_fav_movie):
    
    close_match = difflib.get_close_matches(user_fav_movie.title(), list(movies['title']))
    if bool(close_match):
        user_fav_movie = close_match[0]
        print(user_fav_movie)
        movie_ls=recommend(user_fav_movie)
        print("\n--=-=-=-=-=-=-=-=-==-MOVIE_POSTERS--=-=-=-=-=-=-=-=-==-\n")
        poster_fetch.movie_poster_fetch(movie_ls)
    else: 
        print("no match found!")


