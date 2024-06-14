from flask import Flask, render_template, request
from mtg_set_search import *

app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('template.html')

@app.route('/deckInput', methods=['POST'])
def deckInput():
    decklist = request.form.get('textarea')
    return search_database(decklist)