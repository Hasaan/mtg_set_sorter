from flask import Flask, render_template, request
from mtg_set_search import *

app = Flask(__name__)

@app.route('/', methods=['POST'])
def index():    

    if request.method == 'POST':
        decklist = request.form.get('deckTextArea')
        search_database(decklist)

    return render_template('template.html')

if __name__ == '__main__': 
    app.run() 