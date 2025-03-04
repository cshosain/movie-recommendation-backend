import pandas as pd
from flask.helpers import send_from_directory
from flask_cors import CORS, cross_origin
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity
from flask import Flask, request, render_template, jsonify


def createSimilarity():
    data = pd.read_csv('../templates/main_data.csv') # reading the dataset
    cv = CountVectorizer()
    countMatrix = cv.fit_transform(data['comb'])    # text to vector
    similarity = cosine_similarity(countMatrix) # creating the similarity matrix
    return (data, similarity)


def getAllMovies():
    data = pd.read_csv('../templates/main_data.csv')
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
        lst = list(enumerate(similarity[movieIndex]))   #[(0, 0.00012), (1, 0.00101), (2, 0.00001), ...]
        lst = sorted(lst, key=lambda x: x[1], reverse=True) #[(120, 0.70010), (4951, 0.65002), ...]
        lst = lst[1:20]  # excluding first item since it is the requested movie itself and taking the top20 movies
        movieList = []
        for i in range(len(lst)):
            a = lst[i][0]   #index of the i'th movie among 20movies [(120, 0.70010), ...] to 120,  
            movieList.append(data['movie_title'][a]) #retreve the actual name of the movie of index 120 then 4951 etc.
        return movieList


app = Flask(__name__, static_folder='../templates',
            static_url_path='/')
print("Test",app.static_folder)
CORS(app)

@app.route('/api/movies', methods=['GET'])
@cross_origin()
def movies():
    # returns all the movies in the dataset
    movies = getAllMovies()
    result = {'arr': movies}
    return jsonify(result)


@app.route('/')
@cross_origin()
def serve():
    return send_from_directory(app.static_folder, 'index.html')


@app.route('/api/similarity/<name>')
@cross_origin()
def similarity(name):
    movie = name
    recommendations = Recommend(movie)
    if type(recommendations) == type('string'):
        resultArray = recommendations.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)
    else:
        movieString = '---'.join(recommendations)
        resultArray = movieString.split('---')
        apiResult = {'movies': resultArray}
        return jsonify(apiResult)


@app.errorhandler(404)
def not_found(e):
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == '__main__':
    app.run()
