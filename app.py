from flask import Flask, render_template
from mtg_set_search import *

app = Flask(__name__)

@app.route('/')
def run():
    return search_database('./TestDeck')
