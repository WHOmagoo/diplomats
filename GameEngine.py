from flask import Flask
from flask import request
import json

app = Flask(__name__)

defUrl = '/api/'

@app.route('/')
def test():
    return 'test'

@app.route(defUrl + 'send_order', methods=['POST'])
def send_order():
    if request.is_json:
        content = request.get_json()
        return content['username']
    else:
        return 418
