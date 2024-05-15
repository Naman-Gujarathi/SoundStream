
# gridfs used to store large file , pika is used for rabbitmq
import os, gridfs, pika, json
from flask import Flask, request
#store file in mongodb
from flask_pymongo import PyMongo
from auth import validate
from auth_svc import access
from storage import util


server = Flask(__name__)
server.config("MONGO_URI") = "mongodb://host.minikube.internal:27017/videos"

# PyMongo  manages mongodb connection from flaskapp
mongo = PyMongo(server) 

#by default file more than 16mb stored in mongodb result in performance degradation therefore using fr
# gridfs for storing file largert than 16 mb by sharding the of data into small chunsk 255kb
# GridFS uses two collections one to store file and other to store file metadatat to reassemeble the c# chunk
fs = gridfs.GridFS(mongo.db)

# rabbitmq is opensource message broker , pika library in python is used to connect to rabbitmq
connection = pika.BlockingConnection(pika.ConnectionParameters("rabbitmq"))

# creates channel on established connection which is used to communicate with rabbitmq
channel = connection.channel()

@server.route("/login", methods=[POST])
def login():
  token, err = access.login(request)
  
  if not err:
    return token
  else:
    return err

@server.route("/upload", methods=["POST"])
def upload():
  access, err = validate.token(request)
  # loads converts json string to python object
  access = json.loads(access)
  # if access is admin which is admin claim is true
  if access["admin"]:
    # only one file required
    if len(request.files) > 1 or len(request.files) < 1:
      return "only one file is required", 400
     # Iterate through files, here f is file as value  and _ is key
    for _, f in request.files.items():
 # util module from storage package,  f is file, fs is gridfs, rabbitmq channel and admin access
      err = util.upload(f, fs, channel, access)

      if err:
        return err
    
    return "success!", 200

  else:
    return "not authorized", 401

@server.route("/download", methods=["GET"])
def download():
  pass

if __name__ == "__main__":
  server.run(host="0.0.0.0", port=8080)
   


