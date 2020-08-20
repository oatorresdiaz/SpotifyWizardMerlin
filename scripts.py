import os
import ssl
import csv
import numpy
import urllib.request
from pydub import AudioSegment
from ML import train_segment_classifier_and_create_model, single_file_classification
# from SpotifyAPI import SpotifyAPI


# def create_ml_model():

    # Step 1: Download music from Spotify playlists categorized by the following search terms.

    # search_terms = ['happy', 'sad', 'love', 'beach', 'jazz', 'rock', 'classical']
    #
    # for search_term in search_terms:
    #
    #     download_playlist_music(search_term, 'music/train/' + search_term.replace(' ', '_'))

    # Step 2: Train and create ML model

    # train_segment_classifier_and_create_model('music/train', 'rfMusicGenre')


def download_and_classify_music(search_term, url, track_id, path='music', threshold=0.5):

    print('Classifying track with id ' + track_id + '.')

    path = download_preview_song(url, track_id, path)

    if path:

        class_id, probability, classes = classify_track(path)

        os.remove(path)

        if classes[int(class_id)] == search_term and numpy.max(probability) >= threshold:

            print('Classification of track with id ' + track_id + ' completed.')

            return track_id

    print('Classification of track with id ' + track_id + ' completed.')

    return None


def classify_track(path):

    model_path = 'data/rfMusicGenre'

    return single_file_classification(path, model_path)


# def download_playlist_music(search_term, parent_directory):
#
#     spotify_api = SpotifyAPI()
#
#     playlist = spotify_api.search_playlists(search_term)
#
#     tracks = []
#
#     for playlist in playlist:
#
#         if 'id' in playlist:
#             playlist_id = playlist['id']
#
#             tracks = spotify_api.get_tracks_from_playlist(playlist_id)
#
#     for track in tracks:
#
#         if 'preview_url' in track and track['preview_url'] is not None:
#
#             name = track['name'].replace(' ', '_').replace('\'', '').lower()
#
#             download_preview_song(track['preview_url'], name, parent_directory + '/')


def download_preview_song(url, name, path='/'):
    """
    Downloads mp3 from Spotify library (preview only) and converts it to wav.
    :param url: str
        The url of the mp3. Check Spotify API.
    :param name: str
        The name of the mp3.
    :param path: str
        The path where the file will be downloaded.
    :return dst: str
        The path of the wav file created.
    """

    name = name.replace('.mp3', '').replace(' ', '_').replace('/', '').replace(',', '')

    filename = path + '/' + name + '.mp3'

    print('Downloading ' + filename)

    if not os.path.isdir(path):
        os.makedirs(path)

    context = ssl._create_unverified_context()

    try:
        u = urllib.request.urlopen(url, context=context)
    except:
        return None

    mp3_file = open(filename, 'wb')

    block_size = 8192

    while True:

        buffer = u.read(block_size)

        if not buffer:
            break

        mp3_file.write(buffer)

    mp3_file.close()

    # Convert mp3 to wav

    src = filename
    dst = filename.replace('.mp3', '.wav')

    sound = AudioSegment.from_mp3(src)
    sound.export(dst, format="wav")

    # Delete the old mp3

    os.remove(src)

    return dst


def write_to_csv(filename, fieldnames, data):

    with open(filename, mode='w') as csvfile:

        writer = csv.DictWriter(csvfile, fieldnames)

        writer.writeheader()

        for d in data:

            dict = {}

            for field in fieldnames:
                dict[field] = d[field]

            writer.writerow(dict)