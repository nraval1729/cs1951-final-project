#!/usr/bin/env python3
import sqlite3
import csv
import sys

# Load songs into two arrays and returns them (first array consists of
# an array of tuples, where each tuple represents the features of a
# particular song. second array consists of popularity for a song. indexing
# matches for both arrays for each song).
def load_songs():
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../node/app/database.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_popularity = []

    for song in c.execute('''
                    SELECT spotify_song_popularity, acousticness, danceability, energy,
                    instrumentalness, loudness, mode, speechiness, tempo, valence,
                    liveness
                    FROM songs ORDER BY song_name LIMIT 1000
                '''):

        songs_features.append(song[1:])
        songs_popularity.append(song[0])

    return songs_features, songs_popularity

# Same function as above, but loads the next 10 songs after the initial 1000 songs
# we trained on.
def load_test_songs():
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../node/app/database.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_popularity = []

    for song in c.execute('''
                    SELECT spotify_song_popularity, acousticness, danceability, energy,
                    instrumentalness, loudness, mode, speechiness, tempo, valence,
                    liveness
                    FROM songs ORDER BY song_name LIMIT 10 OFFSET 1000
                '''):

        songs_features.append(song[1:])
        songs_popularity.append(song[0])

    return songs_features, songs_popularity

if __name__ == '__main__':
    songs_features, songs_popularity = load_songs()

    test_features, test_popularity = load_test_songs()
    print(test_popularity)
