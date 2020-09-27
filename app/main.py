# coding: utf-8
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from app.utils import *

app = Flask(__name__)
CORS(app, support_credentials=True)


@app.route('/', methods=['GET']) # To prevent Cors issues
@cross_origin(supports_credentials=True)
def index():
    # Sent in GET requests
    param = request.args.get('param')
    # Build the response
    response = jsonify({ 'status':'success', 'message': 'Welcome to Undelete API.' })
    # Let's allow all Origin requests
    response.headers.add('Access-Control-Allow-Origin', '*') # To prevent Cors issues
    return response


@app.route('/watch', methods=['POST']) # To prevent Cors issues
@cross_origin(supports_credentials=True)
def watch():
    url = request.form.get("url")
    chat_id = request.form.get("chat_id")

    # Let's watch this url
    watch_this(url, chat_id)

    # Build the response
    response = jsonify({ 
        'status':'success', 
        'message': chat_id + ', your tweet "' + url.split("/")[-1] + '" is been watching by UnDelete.'
    })
    # Let's allow all Origin requests
    response.headers.add('Access-Control-Allow-Origin', '*') # To prevent Cors issues
    return response
    

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1122)
