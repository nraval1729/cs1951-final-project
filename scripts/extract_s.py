#!/usr/bin/env python3
import requests
import csv
import time
import sys
import json

import pprint
pp = pprint.PrettyPrinter(indent=4)
# pp.pprint(json_object)
# pp.pprint(array)

prefix_url = 'https://api.spotify.com/v1/'
csv.field_size_limit(sys.maxsize)

def API_get_several_track_request(track_ids):
    '''
    Makes an API call to the Spotify API Search endpoint with a list of track
    ids for additional information for those tracks.
    Returns the response in list format.

    INPUT:
    track_ids - a list of strings representing artist ids
    OUTPUT:
    response object from request (use .json() to extract data)
    '''

    url = prefix_url + 'tracks/'
    params = {'ids': ','.join(track_ids)}
    try:
        resp = requests.get(url, params=params)
    except requests.exceptions.ConnectionError:
       res
    return resp

def API_get_several_albums_request(album_ids):
    url = prefix_url + 'albums/'
    params = {'ids': ','.join(album_ids)}
    resp = requests.get(url, params=params)

    return resp

def API_get_several_artists_request(artist_ids):
    '''
    Makes a Spotify API request to get information on several albums given
    a list of their ids.

    INPUT:
    album_ids - a list of strings representing artist ids
    OUTPUT:
    response object from request (use .json() to extract data)
    '''
    url = prefix_url + 'artists'
    params = {'ids': ','.join(artist_ids)}
    resp = requests.get(url, params=params)

    return resp

def parse_genres(genres_array):
    # All the 5's here refer to the fact that there are 5 columns in the DB for genres
    genres = [''] * 5
    iter_size = min(5, len(genres_array))

    for i in range(0, iter_size):
        genres[i] = genres_array

    return genres

def main():
    track_ids = []
    jams = []

    # Reads jams.tsv and populates track_ids list to search for through Spotify's
    # API
    i = 0
    with open('../data/archive/jams.tsv','rU') as tsvin:
        tsvin = csv.DictReader(tsvin, delimiter='\t')
        for row in tsvin:
            if ((len(row) > 6 and row['spotify_uri'] != '' and row['spotify_uri'])):
                if (row['spotify_uri'][14:] not in track_ids):
                    track_ids.append(row['spotify_uri'][14:])
                i = i + 1
                jams.append(row)

    # Needed for individual API calls on albums and artists in a later step
    album_ids = []
    artist_ids = []

    ###########################################################################
    ###########################################################################
    ##########                                                       ##########
    ##########                       Songs                           ##########
    ##########                                                       ##########
    ###########################################################################
    ###########################################################################
    # Grab spotify data
    print('spotify API: songs')
    song_results = []
    for idx in range(0, len(track_ids), 50):
        response = API_get_several_track_request(track_ids[idx:idx+50])
        if (response.status_code == 200):
            data = response.json()
            if (data['tracks']):
                for track in data['tracks']:
                    song_results.append(track)
                    album_ids.append(track['album']['id'])
                    artist_ids.append(track['artists'][0]['id'])
        time.sleep(0.1)

    # Join jams data w/ spotify data and write to a CSV file
    print('writing songs.csv')
    with open ('../data/songs.csv', 'w', encoding=) as song_csv:
        write_song = csv.writer(song_csv)
        write_song.writerow(['song_id', 'album_id', 'artist_id', 'song_name', 'duration_ms', 'spotify_song_popularity'])
        for song in song_results:
            write_song.writerow([song['id'].encode('utf-8'), song['album']['id'].encode('utf-8'), song['artists'][0]['id'].encode('utf-8'),  song['name'].encode('utf-8'),  song['duration_ms'], song['popularity']])


    ###########################################################################
    ###########################################################################
    ##########                                                       ##########
    ##########                        Jams                           ##########
    ##########                                                       ##########
    ###########################################################################
    ###########################################################################
    with open('../data/jams.csv', 'w') as jam_csv:
        writer = csv.writer(jam_csv)
        writer.writerow(['jam_id', 'song_id', 'creation_date'])
        for jam in jams:
            writer.writerow([jam['jam_id'].encode('utf-8'), jam['spotify_uri'][14:].encode('utf-8'), jam['creation_date'].encode('utf-8')])

if __name__ == '__main__':
    main()
