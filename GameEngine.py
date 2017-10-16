from flask import Flask
import json

app = Flask(__name__)

defUrl = '/api/'

@app.route('/')
def test():
    return 'test';
