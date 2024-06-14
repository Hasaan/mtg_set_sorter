from flask import Flask, render_template, request
from flask_socketio import SocketIO
from mtg_set_search import *

app = Flask(__name__)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app, cors_allowed_origins="*")

@app.route('/', methods=['GET', 'POST'])
def index():   
    if request.method == 'POST':
        decklist = request.form.get('deckText')
        SortedList = search_database(decklist)
        print(SortedList)
        sendList(SortedList)
        
    return render_template('template.html')

if __name__ == '__main__':
    socketio.run(app)

def sendList(listToSend):
    print('sending list:')
    print(listToSend)
    socketio.emit('sortedListupdate', listToSend)


# @app.route('/deckInput', methods=['POST'])
# def deckInput():
#     if request.method == 'POST':
#         decklist = request.form.get('deckTextArea')
#         search_database(decklist)

    
