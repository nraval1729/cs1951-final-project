#!/usr/bin/env python3
import sqlite3
import csv
import sys

csv.field_size_limit(sys.maxsize)

def load():

    ###################################################
    # TODO:                                           #
    # Fill in this function so that it loads your     #
    # data into a file called playlist_data.db.       #
    ###################################################

    conn = sqlite3.connect('../data/database.db')
    conn.text_factory = str
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS "likes"')
    c.execute('DROP TABLE IF EXISTS "followers"')
    c.execute('DROP TABLE IF EXISTS "jams"')
    c.execute('DROP TABLE IF EXISTS "songs"')
    c.execute('DROP TABLE IF EXISTS "artists"')
    c.execute('DROP TABLE IF EXISTS "albums"')

    c.execute('''
            CREATE TABLE likes(
                user_id VARCHAR(25) NOT NULL,
                jam_id VARCHAR(25) NOT NULL,
                PRIMARY KEY (user_id, jam_id),
                FOREIGN KEY (jam_id) REFERENCES jams(jam_id))
            ''')

    c.execute('''
            CREATE TABLE followers(
                followed_user_id VARCHAR(25) NOT NULL,
                follower_user_id VARCHAR(25) NOT NULL)
            ''')

    c.execute('''
            CREATE TABLE jams(
                jam_id VARCHAR(25) NOT NULL,
                song_id VARCHAR(25) NOT NULL,
                creation_date DATE NOT NULL,
                PRIMARY KEY (jam_id),
                FOREIGN KEY (song_id) REFERENCES songs(song_id))
            ''')

    c.execute('''
            CREATE TABLE songs(
                song_id  VARCHAR(25),
                album_id VARCHAR(25),
                artist_id VARCHAR(25),
                song_name VARCHAR(30) NOT NULL,
                duration_ms INTEGER NOT NULL,
                spotify_song_popularity INTEGER NOT NULL,
                acousticness FLOAT(25),
                danceability FLOAT(25),
                energy FLOAT(25),
                instrumentalness FLOAT(25),
                key INTEGER,
                loudness FLOAT(25),
                mode INTEGER,
                speechiness FLOAT(25),
                tempo FLOAT(25),
                time_signature INTEGER,
                valence FLOAT(25),
                liveness FLOAT(25),
                PRIMARY KEY (song_id),
                FOREIGN KEY (album_id) REFERENCES albums(album_id),
                FOREIGN KEY (artist_id) REFERENCES artists(artist_id))
            ''')

    c.execute('''
            CREATE TABLE artists(
                artist_id VARCHAR(25) NOT NULL,
                artist_name VARCHAR(25) NOT NULL,
                artist_image_url DATE NOT NULL,
                spotify_artist_popularity INTEGER NOT NULL,
                PRIMARY KEY (artist_id))
            ''')

    c.execute('''
            CREATE TABLE albums(
                album_id VARCHAR(25) NOT NULL,
                album_name VARCHAR(25) NOT NULL,
                release_date DATE NOT NULL,
                genre1 VARCHAR(25),
                genre2 VARCHAR(25),
                genre3 VARCHAR(25),
                genre4 VARCHAR(25),
                genre5 VARCHAR(25),
                album_image_url VARCHAR(25),
                PRIMARY KEY (album_id))
            ''')

    with open("../data/artists.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute('''
                INSERT OR IGNORE INTO artists
                VALUES (?, ?, ?, ?)
                ''', (row["artist_id"], row["artist_name"], row["artist_image_url"], row["spotify_artist_popularity"]))


    with open("../data/albums.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute('''
                INSERT OR IGNORE INTO albums
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row["album_id"], row["album_name"], row["release_date"], row["genre1"], row["genre2"], row["genre3"], row["genre4"], row["genre5"], row["album_image_url"]))

    #Insert into songs (leave feature attributes as None for initial insert (gets updated below))
    with open("../data/songs.csv", "r") as f:
        reader = csv.DictReader(f)
        for row in reader:
            c.execute('''
                INSERT OR IGNORE INTO songs
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
                ''', (row["song_id"], row["album_id"], row["artist_id"], row["song_name"], row["duration_ms"], row["spotify_song_popularity"], 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0))

    #Insert into jams
    with open('../data/archive/jams.tsv','rU') as tsvin:
        reader = csv.DictReader(tsvin, delimiter='\t')
        for row in reader:
            if (row["spotify_uri"]):
                c.execute('''
                    INSERT OR IGNORE INTO jams
                    VALUES (?, ?, ?)
                    ''', (row["jam_id"], row["spotify_uri"][14:], row["creation_date"]))

    # Insert into likes table
    with open('../data/archive/likes.tsv', 'r') as f:
        reader = csv.DictReader(f, delimiter='\t', quoting=csv.QUOTE_NONE)
        for row in reader:
            c.execute('''
                INSERT OR IGNORE INTO likes
                VALUES (?, ?)
                ''', (row['user_id'], row['jam_id']))

    # Insert into followers
    with open('../data/features.csv', 'r') as f:
        reader = csv.DictReader(f, delimiter=',', quoting=csv.QUOTE_NONE)
        for row in reader:
            c.execute('''
                UPDATE songs
                SET acousticness = ?, danceability = ?, energy = ?, instrumentalness = ?, key = ?, loudness = ?, mode = ?,
                speechiness = ?, tempo = ?, time_signature = ?, valence = ?, liveness = ?
                WHERE song_id = ?
                ''', (row['acousticness'], row['danceability'], row['energy'], row['instrumentalness'], row['key'],
                row['loudness'], row['mode'], row['speechiness'], row['tempo'], row['time_signature'], row['valence'], row['liveness'], row['id']))

    conn.commit()
    conn.close()

    ###################################################
    #               END OF YOUR CODE                  #
    ###################################################

if __name__ == '__main__':
    load()
