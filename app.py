from flask import Flask, render_template
from mtg_set_search import *

app = Flask(__name__)

@app.route('/')
def index():    
    return render_template('template.html')

@app.route('/my-link/')
def my_link():
  print('I got clicked!')

  return 'Click.'