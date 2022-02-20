import logging
import json

import azure.functions as func


# PRE LOAD ML MODELS
import main.helpers.knn_recommender as knnrec
import main.helpers.collabv2 as c2
import main.helpers.itemrecommender as ir


def main(req: func.HttpRequest) -> func.HttpResponse:
    type = req.route_params.get("restOfPath")
    if not type:
        return func.HttpResponse("Please pass a type on the query string", status_code=400)

    name = req.params.get('name')
    if not name:
        try:
            req_body = req.get_json()
        except ValueError:
            pass
        else:
            name = req_body.get('name')
    
    if name:
        if(type == "knn"):
            logging.info("Starting KNN Recommender")
            try:
                output = knnrec.KNN_recommend(name)
            except Exception as e:
                print("GOT AN ERROR IN KNN , ERROR -- ", e)
                x = {"status" :"erorr" , "message" : str(e)}
                k = json.dumps(x)
                return func.HttpResponse(f"Error: {str(k)}", status_code=500)
            return func.HttpResponse(f"{output}", mimetype="application/json")
        elif (type == "svd"):
            logging.info("Starting SVD Recommender")
            try:
                output = c2.svd_recommend(name)
            except Exception as e:
                print("GOT AN ERROR IN SVD , ERROR -- ", e)
                x = {"status" :"erorr" , "message" : str(e)}
                k = json.dumps(x)
                return func.HttpResponse(f"Error: {str(k)}", status_code=500)
            return func.HttpResponse(f"{output}", mimetype="application/json")
        elif (type == "item"):
            logging.info("Starting Item Based Recommender")
            try:
                rc = ir.RecommenderSystem("main/data/movie_dataset.csv", ['keywords','cast','genres','director'])
                output = rc.recommend_movies(movie=name)
            except Exception as e:
                print("GOT AN ERROR IN ITEM , ERROR -- ", e)
                x = {"status" :"erorr" , "message" : str(e)}
                k = json.dumps(x)
                return func.HttpResponse(f"Error: {str(k)}", status_code=500)
            return func.HttpResponse(f"{output}", mimetype="application/json")
        else:
            return func.HttpResponse(f"Required params not defined." , status_code=400)
    else:
        return func.HttpResponse(f"Required params not defined." , status_code=400)


    # if name:
    #     return func.HttpResponse(f"Hello, {name}. This HTTP triggered function executed successfully.")
    # else:
    #     return func.HttpResponse(
    #          "This HTTP triggered function executed successfully. Pass a name in the query string or in the request body for a personalized response.",
    #          status_code=200
    #     )
