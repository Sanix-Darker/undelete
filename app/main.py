# coding: utf-8
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from app.utils import *
from app.model import UnDelete , WatchMe

app = Flask(__name__)
CORS(app, support_credentials=True)

Ud = UnDelete.UnDelete
Wm = WatchMe.WatchMe

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

    # Let's try to watch this url
    # Build the response
    response = jsonify(watch_this(Ud, Wm, url, chat_id))

    # Let's allow all Origin requests
    response.headers.add('Access-Control-Allow-Origin', '*') # To prevent Cors issues
    return response
    

@app.route('/unwatchme', methods=['POST']) # To prevent Cors issues
@cross_origin(supports_credentials=True)
def unwatchme():
    url = request.form.get("url")
    chat_id = request.form.get("chat_id")

    # Let's try to watch this url
    # Build the response
    response = jsonify(unwatch(Ud, Wm, url, chat_id))

    # Let's allow all Origin requests
    response.headers.add('Access-Control-Allow-Origin', '*') # To prevent Cors issues
    return response


if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, port=1122)
