import secrets
from flask import Flask, request
from movieClient import MovieClient
from secret import * 
from flask_httpauth import HTTPBasicAuth
import json
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
auth = HTTPBasicAuth()

users = {ADMIN_USER: generate_password_hash(ADMIN_PASS)}

movieClient = MovieClient(API_KEY,BASE_URL)

@auth.verify_password
def verify_password(username, password):
    if username in users and check_password_hash(users.get(username), password):
        return username

@app.route("/")
@auth.login_required
def health():
    return "healthy"

@app.route("/get-popular-movies")
def getPopularMovies():
    result = movieClient.getReq(BASE_URL + '3/movie/popular?api_key=' + API_KEY + '&language=en-US&page=1')
    content = result.content.decode("utf-8")
    jsonFormat = json.loads(content)
    return json.dumps(jsonFormat['results']), 200

@app.route("/get-similar-movies")
def getSimilarMovies():
    id = str(request.args.get('id'))
    result = movieClient.getReq(BASE_URL + '3/movie/' + id + '/similar?api_key=' + API_KEY + '&language=en-US&page=1')
    content = result.content.decode("utf-8")
    jsonFormat = json.loads(content)
    return json.dumps(jsonFormat['results'][0:5]), 200

@app.route("/get-movie")
def getMovieByID():
    id = str(request.args.get('id'))
    result = movieClient.getReq(BASE_URL + '3/movie/' + id + '?api_key=' + API_KEY + '&language=en-US&page=1')
    content = result.content.decode("utf-8")
    return content, 200

@app.route("/get-search-results")
def getSearchResults():
    query = request.args.get('query')
    result = movieClient.getReq(BASE_URL + '3/search/movie?api_key=' + API_KEY + '&language=en-US&query=' + query + '&page=1&include_adult=false')
    content = result.content.decode("utf-8")
    jsonFormat = json.loads(content)
    return json.dumps(jsonFormat['results'][0:20]), 200
    


