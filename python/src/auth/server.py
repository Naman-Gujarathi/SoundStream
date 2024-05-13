# JWT to create token, datetime to set expiration for token
#os for setting env variable mysql connection  
import jwt, datetime, os 

# websserver used using flask
from flask import Flask, request

# query our database 
from flask_mysqldb import MySQL

#Flask main class of Flask framework, server is instance of Flask
server = Flask(__name__)
#mysql is instance of  create and mySQL(server)it help to set up connection between application#server and MySQL() 
mysql = MySQL(server)

#config
server.config["MYSQL_HOST"]= os.environ.get("MYSQL_HOST")
server.config["MYSQL_USER"]= os.environ.get("MYSQL_USER")
server.config["MYSQL_PASSWORD"]= os.environ.get("MYSQL_PASSWORD")
server.config["MYSQL_DB"]= os.environ.get("MYSQL_DB")
server.config["MYSQL_PORT"]= os.environ.get("MYSQL_PORT")

@server.route("/login", methods = ["POST"])
def login():
    auth = request.authorization
    if not auth:
      return"missing credentilas", 401

    # check db for username and passwrod
    # use cursor to execute queries
    cur = mysql.connection.cursor()
    res = cur.execute(
        "SELECT email, password FROM user WHERE email=%s",(auth.username,)
    )
    # res holds the number of rows affected or returned.
    
# fetchone() method retrieves a single row from the result set and returns as tuple
# cur.fetchone() is to retrieve rows from the cursor, where actual results are held  
    if res > 0:
    	user_row = cur.fetchone()
    	email = user_row[0]
    	password = user_row[1]

    	if auth.username != email or auth.password != password:
            return "invalid credentials", 401
    	else:
            return createJWT(auth.username, os.environ.get("JWT_SECRET"), True)
    else:
        return "invalid credentials", 401
   
@server.route("/validate", methods = ["POST"])
def validate():
   encoded_jwt = request.headers["Authorization"]

   if not encoded_jwt:
      return "missing credentails", 401

   encoded_jwt = encoded_jwt.split(" ")[1]

   try:
      decoded = jwt.decode(
         encoded_jwt, os.environ.get("JWT_SECRET"), algorithm=["HS256"]
      )
   except:
      return "not authorized", 403

   return decoded, 200

def createJWT(username, secret, authz):
   return jwt.encode(
    {
      "username" : username,
      "exp": datetime.datetime.now(tz = datetime.timezone.utc) + datetime.timedelta(       days=1),
      "iat": datetime.datetime.utcnow(),
      "admin": authz,
    },
    secret,
    algorithm ="HS256"
   )

if __name__ == "__main__":
   server.run(host="0.0.0.0", port=5000)    
