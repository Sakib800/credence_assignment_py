from flask import Flask,Response,request
import pymongo
import json
from bson.objectid import ObjectId
# from bson.json_util import dumps
# from bson.json_util import loads
app = Flask(__name__)

try:
    mongo=pymongo.MongoClient(host="localhost",port=27017,serverSelectionTimeoutMS = 1000 )
    db = mongo.movie_store
    mongo.server_info() #it throws an error when it does not  gets connected to the db

except:
    print("Error - Cannot connect to db")
  ##################POST METHOD STARTS 
@app.route("/movies", methods=["POST"])
def create_movie():
    try:
        movie ={"name":request.form["name"], "img":request.form["img"],"summary":request.form["summary"]}
        dbResponse = db.movies.insert_one(movie)  
        return Response(
            response= json.dumps({"message":"movie created","id":f"{dbResponse.inserted_id}"}) ,
            status=200,
            mimetype= "application/json"
        )
    except Exception as ex:
        print("************")
        print(ex)
        print("************")

          ##################START GET METHOD
@app.route("/movies", methods=["GET"])
def get_some_movies():
    try:
        movieList = list(db.movies.find())
        for movie in movieList:
            movie["_id"]=str(movie["_id"])
        # return data
        # jsonData = (loads(dumps(data)))
        # print(jsonData)
        return Response(
            response = json.dumps(movieList),
    status = 200,
    mimetype="apllication/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"cannot read movies"}),
                        status=500,
                        mimetype="application/json" )
  
    ###########################END GET METHOD


    #########################GET METHOD FOR SPECIFIC#####
@app.route("/movies/<id>", methods=["GET"])
def get_movies(id):
    try:
        movie = db.movies.find_one({'_id': ObjectId(id)})
        movie["_id"] = str( movie["_id"] )
        return Response(
            response = json.dumps(movie),
            
    status = 200,
    mimetype="apllication/json")
    except Exception as ex:
        print(ex)
        return Response(response = json.dumps({"message":"cannot read the requested movie"}),
                        status=500,
                        mimetype="application/json" )
    
    #########################END GET SPECIFIC#########


##########################PATCH START HERE
@app.route("/movies/<id>", methods=["PATCH"])
def update_movie(id):
#   return id
  try:
      dbResponse = db.movies.update_one(
          {"_id":ObjectId(id)},
          {"$set":{"name":request.form["name"], "img":request.form["img"],"summary":request.form["summary"]}}
      )
      return Response(
      response = json.dumps({"message":"movie updated"}),   
      status = 200,
      mimetype="application/json"
     )

  except Exception as ex:
      print("************")
      print(ex)
      print("************")
      return Response(
            response= json.dumps({"message":"cannot Update the movie"}) ,
            status=500,
            mimetype= "application/json"
      )
####################DELETE START HERE##
 
@app.route("/movies/<id>", methods=["DELETE"])
def delete_movie(id):
    try:
        dbResponse = db.movies.delete_one({"_id":ObjectId(id)})
        return Response(
      response = json.dumps({"message":"movie deleted"}),   
      status = 200,
      mimetype="application/json"
     )
    except Exception as ex:
        
      print("************")
      print(ex)
      print("************")
      return Response(
            response= json.dumps({"message":"cannot delete"}) ,
            status=500,
            mimetype= "application/json"
      )


##################################
###start the server

if __name__ == "_main_":
    app.run(port=80,debug=True)