import os
import numpy
import json
import asyncio
from flask import Flask, request
from flask_cors import CORS, cross_origin
from scripts import download_and_classify_music

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'


@app.route('/')
def route():

    return {'hello': 'world'}


@app.route('/classify-music', methods=['POST'])
@cross_origin()
def classify_music():

    if request.json is not None:

        if 'search_term' in request.json and 'track_meta' in request.json:

            print('Received new request.')

            search_term = request.json['search_term']

            track_meta = request.json['track_meta']

            loop = asyncio.new_event_loop()

            asyncio.set_event_loop(loop)

            classification_processes = [download_and_classify_music(search_term, meta[1], meta[0]) for meta in track_meta]

            results = loop.run_until_complete(asyncio.gather(*classification_processes))

            loop.close()

            res = []

            for result in results:

                if result:

                    res.append(result)

            return json.dumps(res)


if __name__ == "__main__":
    if os.environ.get('IS_HEROKU'):
        app.run()
    else:
        app.run(debug=True, use_debugger=True, port=5001)

