from importlib.abc import ResourceLoader
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
@auth.login_required
def getPopularMovies():
    result = movieClient.getReq(BASE_URL + '3/movie/popular?api_key=' + API_KEY + '&language=en-US&page=1')
    if result.status_code == 200:
        content = result.content.decode("utf-8")
        jsonFormat = json.loads(content)
        return json.dumps(jsonFormat['results']), 200
    return 'something went wrong', 500

@app.route("/get-similar-movies")
@auth.login_required
def getSimilarMovies():
    if request.args.get('id'):
        id = str(request.args.get('id'))
    else:
        return 'missing required arguments', 422
    result = movieClient.getReq(BASE_URL + '3/movie/' + id + '/similar?api_key=' + API_KEY + '&language=en-US&page=1')
    if result.status_code == 200:
        content = result.content.decode("utf-8")
        jsonFormat = json.loads(content)
        return json.dumps(jsonFormat['results'][0:5]), 200
    return 'something went wrong', 500

@app.route("/get-movie")
@auth.login_required
def getMovieByID():
    if request.args.get('id'):
        id = str(request.args.get('id'))
    else:
        return 'missing required arguments', 422
    result = movieClient.getReq(BASE_URL + '3/movie/' + id + '?api_key=' + API_KEY + '&language=en-US&page=1')
    if result.status_code == 200:
        content = result.content.decode("utf-8")
        return content, 200
    else:
        return 'something went wrong', 500

@app.route("/get-search-results")
@auth.login_required
def getSearchResults():
    if request.args.get('query'):
        query = request.args.get('query')
    else:
        return 'missing required arguments', 422
    result = movieClient.getReq(BASE_URL + '3/search/movie?api_key=' + API_KEY + '&language=en-US&query=' + query + '&page=1&include_adult=false')
    if result.status_code == 200:
        content = result.content.decode("utf-8")
        jsonFormat = json.loads(content)
        return json.dumps(jsonFormat['results'][0:20]), 200
    return 'something went wrong', 500
if __name__ == '__main__':
    app.run()

