from flask import Flask, render_template, request, jsonify, Response, redirect, url_for
import pickle
import os
app = Flask(__name__)


@app.route('/')
def hello_world():
    return render_template('home.html')


@app.route('/year')
def search():
    return render_template('year.html')


@app.route('/artist')
def search2():
    # artist_names = ['Albrecht_Durer', 'Alfred_Sisley', 'Claude_Monet']
    with open('artist_names', 'rb') as handle:
        artist_names = pickle.load(handle)
        print(artist_names)
    return render_template('artist.html', artist_names=artist_names)


@app.route('/genre')
def search3():
    with open('genres', 'rb') as handle:
        genres = pickle.load(handle)
    return render_template('genre.html', genres=list(genres))


@app.route('/nationality')
def search4():
    return render_template('nationality.html')


if __name__ == '__main__':
    app.run()
