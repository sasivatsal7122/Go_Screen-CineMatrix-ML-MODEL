import knn_recommender as knnrec
import itemrecommender as ir
import collabv1 as c1
import collabv2 as c2
import tfidf_lk as tlk


user_movie=input("Enter you're fav movie: ")


print("\n```````````````STARTED ITEM BASED RECOMMENDER```````````````\n")
''' CALLING ITEM BASED RECOMMENDER'''
rc = ir.RecommenderSystem("Datasets/movie_dataset.csv", ['keywords','cast','genres','director'])
rc.recommend_movies(movie=user_movie)


print("\n```````````````STARTED SVD RECOMMENDER```````````````\n")
''' CALLING SVD RECOMMENDER'''
c2.svd_recommend(user_movie)


print("\n```````````````STARTED KNN RECOMMENDER```````````````\n")
''' CALLING KNN RECOMMENDER '''
knnrec.KNN_recommend(user_movie)


print("\n```````````````STARTED TFIDF_LINEAR_KERNERL RECOMMENDER```````````````\n")
''' CALLING TFIDF_LK RECOMMENDER '''
tlk.tfidf_lk_recommend(user_movie)


print("\n```````````````STARTED COLLABRATIVE CORRELATION RECOMMENDER```````````````\n")
''' CALLING CORRELATION BASED RECOMMENDER'''
crc = c1.collabrative_filtering("Datasets/huge_cmovies_dataset.csv")
crc.get_user_movie(user_movie)
crc.recommend_movies()





