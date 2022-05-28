import difflib
from tkinter.font import names
from flask import Flask, render_template, Request
import pickle
import flask
from numpy import char
import pandas as pd
import json
import jinja2
from jinja2 import Template
# create flask app
app = Flask(__name__)

movies_dict = pickle.load(open('Movies.pkl','rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl','rb'))

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:11]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

@app.route('/')
def index():
   return render_template('index.html')

@app.route('/final',methods=['POST'])
def final():
     if flask.request.method =='GET':
         return render_template('index.html')
    
     if flask.request.method =='POST':
        movie_names = flask.request.form['movie_name']
        movie_names = movie_names.title()
        print(movie_names)
        result_final = recommend(movie_names)

        name = []
        for i in range(len(result_final)):
           name.append(result_final[i] )
        return render_template('result.html',movie_names=name,search_name=movie_names)

if __name__ == '__main__':
    app.run(debug=True)