#!/usr/bin/env python3
import sqlite3
import csv
import sys
import unicodedata
#from unidecode import unidecode

#tsv jams: 2.095
#1479780

csv.field_size_limit(sys.maxsize)

def strip_accents(s):
   return ''.join(c for c in unicodedata.normalize('NFD', s)
                  if unicodedata.category(c) != 'Mn')

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
        with open('../data/archive/jams.tsv','rU') as tsvin2:
            reader = csv.DictReader(tsvin, delimiter='\t')
            for row in reader:
                spotify_uri = row["spotify_uri"]
                print (spotify_uri)
                if (not row["spotify_uri"] and row["title"] and row["artist"]):
                    tsvin2.seek(0)
                    reader2 = csv.DictReader(tsvin2, delimiter='\t')
                    for row2 in reader2:
                        if (row2["artist"] and row2["title"]):
                            artist1 = strip_accents((row["artist"]))
                            artist2 = strip_accents((row2["artist"]))
                            song = strip_accents((row["title"]))
                            song2 = strip_accents((row2["title"]))
                    
                            if (row2["spotify_uri"] and (song == song2) and (artist1 == artist2)):
                                spotify_uri = row2["spotify_uri"]
                            
                print (spotify_uri)
                if (spotify_uri):
                    c.execute('''
                        INSERT OR IGNORE INTO jams
                        VALUES (?, ?, ?)
                        ''', (row["jam_id"], spotify_uri[14:].encode("utf-8"), row["creation_date"]))
    conn.commit()
    conn.close()

if __name__ == '__main__':
    load()
