#!/usr/bin/env python3
import sqlite3
import csv
import sys

# Load songs into an array and returns it (data structure consists of
# an array of tuples, where each tuple represents the features of a
# particular song).
def load_songs():
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../node/app/database.db')
    conn.text_factory = str
    c = conn.cursor()
    songs = []
    for song in c.execute('''
                    SELECT spotify_song_popularity, acousticness, danceability, energy,
                    instrumentalness, loudness, mode, speechiness, tempo, valence,
                    liveness
                    FROM songs
                '''):
        songs.append(song)

    return songs

if __name__ == '__main__':
    list_of_songs = load_songs()
    print(list_of_songs)
