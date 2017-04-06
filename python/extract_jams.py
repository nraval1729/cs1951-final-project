#!/usr/bin/env python3
import sqlite3
import csv
import sys
from unidecode import unidecode

reload(sys)
sys.setdefaultencoding("utf-8")
csv.field_size_limit(sys.maxsize)

def load():

    conn = sqlite3.connect('../data/database.db')
    conn.text_factory = str
    c = conn.cursor()

    c.execute('DROP TABLE IF EXISTS "jams"')

    c.execute('''
            CREATE TABLE jams(
                jam_id VARCHAR(25) NOT NULL,
                song_id VARCHAR(25) NOT NULL,
                creation_date DATE NOT NULL,
                PRIMARY KEY (jam_id),
                FOREIGN KEY (song_id) REFERENCES songs(song_id))
            ''')


    with open('../data/archive/jams.tsv','rU') as tsvin:
            reader = csv.DictReader(tsvin, delimiter='\t')
            for row in reader:
                spotify_uri = row["spotify_uri"]
                if (not row["spotify_uri"] and row[]):
                    for row2 in reader:
                        artist1 = unidecode(row["artist"])
                        artist2 = unidecode(row2["artist"])
                        song = unidecode(row["title"])
                        song2 = unidecode(row2["title"])
                
                        if (row2["spotify_uri"] and (song == song2) and (artist == artist2)):
                            spotify_uri = row2["spotify_uri"]

                        if row["artist"] != artist1:
                            print (artist1)
                            print (row["artist"])
                            print (spotify_uri)
                if (spotify_uri):
                    c.execute('''
                        INSERT OR IGNORE INTO jams
                        VALUES (?, ?, ?)
                        ''', (row["jam_id"], spotify_uri[14:], row["creation_date"]))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    load()
