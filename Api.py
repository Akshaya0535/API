from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
from flask_ngrok import run_with_ngrok
from flask import make_response
import random

## Add Authentication 
from flask_httpauth import HTTPBasicAuth

## Auth Code Start
auth = HTTPBasicAuth()

# Add Users
users = {
    "ali": "iali.dev",
    "public": "public"
}

# Get Password mechanism 
@auth.get_password
def get_pass(username):
    if username in users:
        return users.get(username)
    return None

## Auth Code End

app = Flask(__name__)
api = Api(app)

dev_jokes = [
    {
        "id": 0,
        "author": "NA",
        "joke": "Q: How did the Coder CEO build his company headquarters? A: By calling the Constructor();", 
        "source": "https://github.com/shrutikapoor08/devjoke/blob/master/README.md"
    },
    {
        "id": 1,
        "author": "NA",
        "joke": "Q: What is Hardware? A: The part of the computer which you can kick.",
        "source": "https://github.com/shrutikapoor08/devjoke/blob/master/README.md"
    },
    {
        "id": 2,
        "author": "NA",
        "joke": "Q: Who is a programmer? A: A programmer is a machine who turns coffee into code.",
        "source": "https://github.com/shrutikapoor08/devjoke/blob/master/README.md"
    },
    {
        "id": 3,
        "author": "NA",
        "joke": "First rule of programming : If it works DON'T touch it.",
        "source": "https://github.com/shrutikapoor08/devjoke/blob/master/README.md"
    }
]

class joke(Resource):
    def get(self, id=0):
        if not id:
            return random.choice(dev_jokes), 200
        for joke in dev_jokes:
            if(joke["id"] == id):
                return joke, 200
        return "Joke not found", 404
      
class adjoke(Resource):
    @auth.login_required
    def post(self):
      parser = reqparse.RequestParser()
      parser.add_argument("id",type=int,required=True)
      parser.add_argument("author",required=True)
      parser.add_argument("joke",required=True)
      parser.add_argument("source")
      params = parser.parse_args()
      id = params["id"]
      for joke in dev_jokes:
          if(id == joke["id"]): 
              return make_response(jsonify({'error': 'Joke with this id already exists add new id'}), 400)
      joke = {
          "id": int(id),
          "author": params["author"],
          "joke": params["joke"],
          "source": params["source"]
      }
      dev_jokes.append(joke)
      return joke, 201

    def put(self):
      parser = reqparse.RequestParser()
      parser.add_argument("id",type=int,required=True)
      parser.add_argument("author",required=True)
      parser.add_argument("joke",required=True)
      parser.add_argument("source")      
      params = parser.parse_args()
      id = int(params["id"])
      for obj in dev_jokes:
          if(id == obj["id"]):
              obj["author"] = params["author"]
              obj["joke"] = params["joke"]
              obj["source"] = params["source"]
              return obj, 204
      else:
            return make_response(jsonify({'error': 'ID is not present in database'}), 404)

    def delete(self, id='c'):
        if id is 'c':
          return make_response(jsonify({'error': 'ID is missing'}), 400)
        global dev_jokes
        dev_jokes = [joke for joke in dev_jokes if joke["id"] != id]
        return f"Joke with id {id} is deleted.", 200


class home(Resource):
  def get(self):
    return "Hey there! This is a simple demo for making an API server made by Ali Mustufa Shaikh;"

api.add_resource(joke, "/joke", "/joke/", "/joke/")
api.add_resource(home,"/")
api.add_resource(adjoke,"/adjoke/","/adjoke/","/adjoke")

# For Error Handling Best Practises

@app.errorhandler(404)
def not_found(error):
    return make_response(jsonify({'error': 'Not found'}), 404)

@auth.error_handler
def unauthorized():
    return make_response(jsonify({'error': 'Unauthorized Access'}), 401)


if __name__ == '__main__':
    run_with_ngrok(app)
    app.run()
