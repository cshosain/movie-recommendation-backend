import os
import pandas as pd
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template, jsonify

# Dynamically get the CSV path
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_PATH = os.path.join(BASE_DIR, 'main_data.csv')

def createSimilarity():
    data = pd.read_csv(DATA_PATH)  # Correct path
    cv = CountVectorizer()
    countMatrix = cv.fit_transform(data['comb'])
    similarity = cosine_similarity(countMatrix)
    return data, similarity

def getAllMovies():
    data = pd.read_csv(DATA_PATH)
    return list(data['movie_title'].str.capitalize())

def Recommend(movie):
    movie = movie.lower()
    try:
        data.head()
        similarity.shape
    except:
        (data, similarity) = createSimilarity()
    if movie not in data['movie_title'].unique():
        return 'Sorry! The movie you requested is not present in our database.'
    else:
        movieIndex = data.loc[data['movie_title'] == movie].index[0]
        lst = list(enumerate(similarity[movieIndex]))
        lst = sorted(lst, key=lambda x: x[1], reverse=True)
        lst = lst[1:20]
        movieList = [data['movie_title'][i[0]] for i in lst]
        return movieList

app = Flask(__name__, static_folder=os.path.join(BASE_DIR, '../templates'))
CORS(app)

@app.route('/api/movies', methods=['GET'])
@cross_origin()
def movies():
    return jsonify({'arr': getAllMovies()})

@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')

@app.route('/api/similarity/<name>')
@cross_origin()
def similarity(name):
    recommendations = Recommend(name)
    if isinstance(recommendations, str):
        return jsonify({'movies': recommendations.split('---')})
    else:
        return jsonify({'movies': recommendations})

@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()
