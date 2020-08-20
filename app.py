import os
import numpy
import json
from flask import Flask, request
from flask_cors import CORS, cross_origin
from scripts import download_preview_song, classify_track

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

        results = []

        if 'search_term' in request.json and 'track_meta' in request.json:

            print('Received new request.')

            search_term = request.json['search_term']

            track_meta = request.json['track_meta']

            for index, meta in enumerate(track_meta):

                print('Classifying track ' + str(index + 1) + ' out of ' + str(len(track_meta)) + '.')

                track_id = meta[0]

                track_preview_url = meta[1]

                path = download_preview_song(track_preview_url, track_id, 'music')

                if path:

                    class_id, probability, classes = classify_track(path)

                    if classes[int(class_id)] == search_term:

                        if numpy.max(probability) >= 0.5:

                            results.append(track_id)

                    os.remove(path)

                else:

                    print('Could not download track preview with id: ' + track_id)

            print('Classification completed.')

            return json.dumps(results)


if __name__ == "__main__":
    if os.environ.get('IS_HEROKU'):
        app.run()
    else:
        app.run(debug=True, use_debugger=True, port=5001)

