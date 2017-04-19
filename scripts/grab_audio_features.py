import csv
import json
import requests
from spotipy import oauth2
import spotipy
from collections import OrderedDict
import time
import sys

csv.field_size_limit(sys.maxsize)

client_id = 'add45374bb9640219cddec86caf7d1ce'
client_secret = 'd6a3209a182c499bb157a5c215871b45'

client_credentials_manager = oauth2.SpotifyClientCredentials(client_id, client_secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


def main():
    track_ids = populate_track_ids()

    print "track ids are populated"
    print "Their len: ", len(track_ids)

    features = get_all_features(track_ids)

    print "writing features to files now"

    write_features_to_file(features)

def write_features_to_file(features):
    with open("features.csv", "w") as fcsv:
        fieldnames = ['id','acousticness', 'danceability', 'energy','instrumentalness', 'key', 'liveness', 'loudness', 'mode', 'speechiness', 'tempo', 'time_signature', 'valence', 'analysis_url']

        writer = csv.DictWriter(fcsv, fieldnames=fieldnames)
        writer.writeheader()

        for feature in features:
            # print "This:************************ ", feature
            writer.writerow(feature)




def populate_track_ids():
    track_ids = set()
    # with open("../data_cut/archive/jams.tsv", 'rU') as tsvin:
    with open("../data_cut/archive/jams_slightly_big.tsv", "rU") as tsvin:
        tsvin = csv.DictReader(tsvin, delimiter='\t')
        for row in tsvin:
            # print("Row spotify uri: ", row['spotify_uri'])
            if row and row['spotify_uri']:
                # print index, row['spotify_uri']
                uri = row['spotify_uri'].split(':')[-1]
                # print("Index, Uri: ", index, uri)
                track_ids.add(uri)

    return list(track_ids)

def get_all_features(track_ids):
    list_of_feature_dicts = []
    for idx in range(0, len(track_ids), 50):
        print idx
        # print("inside get all features loop")
        print "Sending these ids: ", track_ids
        response = sp.audio_features(track_ids[idx:idx+50])
        if response:
            # for r, tid in zip(response, track_ids[idx:idx+50]):
            #     print "Tid, r: ", tid, ": ", r
            for r in response:
                if r:
                    curr_dict = OrderedDict()
                    curr_dict['id'] = r['id']
                    curr_dict['acousticness'] = r['acousticness']
                    curr_dict['danceability'] = r['danceability']
                    # curr_dict['duration_ms'] = r['duration_ms']
                    curr_dict['energy'] = r['energy']
                    curr_dict['instrumentalness'] = r['instrumentalness']
                    curr_dict['key'] = r['key']
                    curr_dict['liveness'] = r['liveness']
                    curr_dict['loudness'] = r['loudness']
                    curr_dict['mode'] = r['mode']
                    curr_dict['speechiness'] = r['speechiness']
                    curr_dict['tempo'] = r['tempo']
                    curr_dict['time_signature'] = r['time_signature']
                    curr_dict['valence'] = r['valence']
                    curr_dict['analysis_url'] = r['analysis_url']

                    list_of_feature_dicts.append(curr_dict)

        time.sleep(0.1)

    return list_of_feature_dicts




    return None

if __name__ == "__main__":
    main()

