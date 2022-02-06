# Importing libraries
import pandas as pd
import numpy as np
import difflib
from sklearn.feature_extraction.text import TfidfVectorizer,CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import collab
from collab import *


class RecommenderSystem(object):
    # initializer
    def __init__(self, file_path, cols_list):
        # creating an instance dataframe
        self.movies_df = pd.read_csv(file_path)
        # creating a new col in instance dataframe (self.movies_df)
        self.movies_df['popularity'] =self.movies_df['popularity'].astype(str)
        # defining_features are the columns on which the recommender system focuses on
        self.defining_features = cols_list

        # combined_features is the result of adding all the defining feature column for each movie
        self.combined_features = ''

        # filling null values in the defining features columns of the dataset
        self.clean_df = self.movies_df[self.defining_features].fillna('')

        self.user_movie = ''

        self.create_index_col()

    def get_user_movie(self):
        # movies are recommended based on this movie
        self.user_movie = input("Enter your favourite movie: ")
        return self.user_movie

    def get_index(self, movie):
        # getting the index of the closest match (input)
        return self.movies_df[self.movies_df['title'] == movie]['index'].values[0]
    
    def create_index_col(self):
        # every dataset need not have index columns 
        # so if there is no index column in that dataset,
        # we create one, so that movies can be uniquely identified
        if 'index' in self.movies_df.columns:
            return
        self.movies_df['index'] = np.arange(self.movies_df.shape[0])

    def recommend_movies(self, movie, number_of_movies):
        for feature in self.defining_features:
            self.combined_features += self.clean_df[feature]

        # transforming combined_features' textual data to numerical values
        # so that it's easier for the computer to process
        v = TfidfVectorizer()
        cv = CountVectorizer()
        transformed_features = v.fit_transform(self.combined_features)
        transformed_features_2 = cv.fit_transform(self.combined_features)
        # finding similarities between the movies using the cosine_similarity
        similarity = cosine_similarity(transformed_features)
        similarity_2 = cosine_similarity(transformed_features_2)

        # if the movie name entered by the user
        # may not match exactly with the titles we have in our dataset
        # so closest matches can be found using difflib library
        close_matches = difflib.get_close_matches(movie, list(self.movies_df['title']))
        if not close_matches:
            print("no matches found!")
            return
        closest_match = close_matches[0]

        # similar movies to closest match can be known only when we know the index of this movie
        movie_index = self.get_index(closest_match)
        # similar movies are sorted in descending order
        similar_movies = list(enumerate(similarity[movie_index]))
        similar_movies_2 = list(enumerate(similarity_2[movie_index]))
        
        sorted_similar_movies = sorted(similar_movies, key=lambda x: x[1], reverse=True)
        sorted_similar_movies_2 = sorted(similar_movies_2, key=lambda x: x[1], reverse=True)

        print(f"\nMovies recommended for you: \n")
        final_list=[]
        final_list_2=[]

        for i in range(number_of_movies):
            # extracting the title of the movie using it's index
            index = sorted_similar_movies[i][0]
            movie = self.movies_df[self.movies_df['index'] == index]['title'].values[0]
            final_list.append(movie)
        
            index_2 = sorted_similar_movies_2[i][0]
            movie_2 = self.movies_df[self.movies_df['index'] == index_2]['title'].values[0]
            final_list_2.append(movie_2)
        
        final_list_2.pop(0)
        final_list.pop(0)
        combined_list = final_list + list(set(final_list_2) - set(final_list))
        
        for movie in combined_list:
            print(movie)

# based on 'keywords','cast','genres','director'
# making object rc from class RecommenderSystem
rc = RecommenderSystem("movie_dataset.csv", ['keywords','cast','genres','director'])
# taking input from the user using get_user_movie method in RecommenderSystem class with object rc
user_movie = rc.get_user_movie()
collab.crc.get_user_movie(user_movie)
# defining how many recommendations
number_of_movies = 10
# calling the recommend_movies method in RecommenderSystem class with object rc
rc.recommend_movies(user_movie, number_of_movies)
#collab.crc.recommend_movies()