# importing libraries
import pandas as pd
import numpy as np
import seaborn as sns
import difflib
import poster_fetch
from poster_fetch import *

class collabrative_filtering:
    def __init__(self,file_path):
        self.cmovies_df = pd.read_csv(file_path)
        self.ratings = pd.DataFrame(self.cmovies_df.groupby('title')['rating'].mean())
    
    def get_user_movie(self,x):
        # movies are recommended based on this movie
        self.user_fav_movie = x
    
    def recommend_movies(self):
        
        self.ratings['number_of_ratings'] = self.cmovies_df.groupby('title')['rating'].count()
        movie_matrix = self.cmovies_df.pivot_table(index='userId', columns='title', values='rating')
        self.ratings.sort_values('number_of_ratings', ascending=False).head(30)
        close_match = difflib.get_close_matches(self.user_fav_movie.title(), list(self.cmovies_df['title']))
        if bool(close_match):
            user_fav_movie_ratings = movie_matrix[close_match[0]]
            similar_to_user_fav_movie = movie_matrix.corrwith(user_fav_movie_ratings)
            corr_user_fav_movie = pd.DataFrame(similar_to_user_fav_movie, columns=['correlation'])
            corr_user_fav_movie.dropna(inplace=True)
            corr_user_fav_movie = corr_user_fav_movie.join(self.ratings['number_of_ratings'])
            recommendation_movies = corr_user_fav_movie[corr_user_fav_movie['number_of_ratings'] > 100].sort_values(by='correlation', ascending=False).head(20)
            final = recommendation_movies.iloc[:11,:0]
            final_list=[]
            print("\n====================================================================")   
            print(f"Correlation based Recommended movies based on the {self.user_fav_movie} are:") 
            print("====================================================================\n") 
            for i in range(1,11):
                row = final.index[i]
                final_list.append(row)
            for movies in final_list:
                print(movies)
            #print(final_list)
            print("\n--=-=-=-=-=-=-=-=-==-MOVIE_POSTERS--=-=-=-=-=-=-=-=-==-\n")
            poster_fetch.movie_poster_fetch(final_list)

        else:
            print("\ncouldn't find any matches!")
    
    def plots(self):
        self.ratings['rating'].hist(bins=50)
        self.ratings['number_of_ratings'].hist(bins=60)
        sns.jointplot(x='rating', y='number_of_ratings', data=self.ratings)
        
