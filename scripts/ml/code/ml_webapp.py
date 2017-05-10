#!/usr/bin/env python3
from __future__ import division
import sqlite3
import csv
import sys
import csv
import argparse
from collections import defaultdict
import util
import numpy
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from tokenizer import Tokenizer
import pickle

genre_list = {}
# Based on parameters that were sent from the web app, create a
# a query that returns the correct information for features to use
def choose_query(useGenre, useDance, useEnergy, useLoudness, useArtist):
    query = "SELECT song_hotness,"
    if useGenre:
        query += " artist_mbtags,"
    if useDance:
        query += " danceability,"
    if useEnergy:
        query += " energy,"
    if useLoudness:
        query += " loudness * loudness,"
    if useArtist:
        query += " artist_familiarity,"

    query += " tempo, key, tempo * key, mode, duration, time_signature  FROM songs ORDER BY track_id"

    return query

# # Load songs into two arrays and returns them (first array consists of
# # an array of tuples, where each tuple represents the features of a
# # particular song. second array consists of popularity for a song. indexing
# # matches for both arrays for each song).
def load_songs(useGenre, useDance, useEnergy, useLoudness, useArtist, training, binary):
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../data/songs.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_popularity = []

    query = choose_query(useGenre, useDance, useEnergy, useLoudness, useArtist)

    if training:
        query += " LIMIT 10000"
    else:
        query += " LIMIT 5000 OFFSET 10000"

    print (query)
    for song in c.execute(query):
        #print (song)
        if (song[0] and not math.isnan(float(song[0]))):


            #GENRE Features
            if (useGenre):
                features = list(float(f) for f in song[1:])
                genre_features = ([0] * len(genre_list))
                features_combine = features[:]
                features_combine.extend(genre_features)

                genres = song[1].split(',')
                if (song[1]):
                    for g in genres:
                        features_combine[(len(features) + genre_list[g.strip()])] += 1
            else:
                features_combine = list(float(f) for f in song[1:])

            int_song = 0
            songs_features.append(tuple(features_combine))
            if (binary):
                if (int( 100 * float(song[0])) > 55.0 and binary):
                    int_song = 1
            else:
                int_song = int( 100 * float(song[0]))
            songs_popularity.append(int_song)

    return songs_features, songs_popularity

if __name__ == '__main__':
    with open("../../../genres.txt") as genre_in:
        genres = genre_in.readline()
        i = 0
        while (genres):
            genre = genres.rstrip()
            genre_list[genre] = i
            i += 1
            genres = genre_in.readline()
    songs_features, songs_labels = load_songs(False, False, False, True, True, True, True)

# See: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
# Source: http://www.goliatone.com/blog/2015/04/04/python-parse-boolean-values-with-argparse/
def str2bool(str):
  #susendberg's function
  return str.lower() in ("yes", "true", "t", "1")

def main():
    #Load all genres into a dictionary
    with open("../../../genres.txt") as genre_in:
        genres = genre_in.readline()
        i = 0
        while (genres):
            genre = genres.rstrip()
            genre_list[genre] = i
            i += 1
            genres = genre_in.readline()

    # Load training text and training labels
    training_features, training_labels = load_songs(False, False, False, True, True, True, True)
    count = 0.0
    training_features2, training_labels2 = load_songs(False, False, False, True, True, True, False)

    average_popular = {"artist_popularity" : 0, "loudness" : 0, "tempo":  0, "key": 0, "tempoXkey": 0, "mode" : 0, "duration": 0, "time_signature": 0}
    average_unpopular = {"artist_popularity" : 0, "loudness" : 0, "tempo":  0, "key": 0, "tempoXkey": 0, "mode" : 0, "duration": 0, "time_signature": 0}

    for i in range(0, len(training_labels)):
        if training_labels[i] == 1:
            count += 1.0
            print (training_features[i])
            average_popular["artist_popularity"] += training_features[i][1]
            average_popular["loudness"] += training_features[i][0]
            average_popular["tempo"] += training_features[i][2]
            average_popular["key"] += training_features[i][3]
            average_popular["tempoXkey"] += training_features[i][4]
            average_popular["mode"] += training_features[i][5]
            average_popular["duration"] += training_features[i][6]
            average_popular["time_signature"] += training_features[i][7]
        else:
            average_unpopular["artist_popularity"] += training_features[i][1]
            average_unpopular["loudness"] += training_features[i][0]
            average_unpopular["tempo"] += training_features[i][2]
            average_unpopular["key"] += training_features[i][3]
            average_unpopular["tempoXkey"] += training_features[i][4]
            average_unpopular["mode"] += training_features[i][5]
            average_unpopular["duration"] += training_features[i][6]
            average_unpopular["time_signature"] += training_features[i][7]

    len_label = len(training_labels)

    average_popular["artist_popularity"] /= len_label
    average_popular["loudness"] /= len_label
    average_popular["tempo"] /= len_label
    average_popular["key"] /= len_label
    average_popular["tempoXkey"] /= len_label
    average_popular["mode"] /= len_label
    average_popular["duration"] /= len_label
    average_popular["time_signature"] /= len_label

    average_unpopular["artist_popularity"] /= len_label
    average_unpopular["loudness"] /= len_label
    average_unpopular["tempo"] /= len_label
    average_unpopular["key"] /= len_label
    average_unpopular["tempoXkey"] /= len_label
    average_unpopular["mode"] /= len_label
    average_unpopular["duration"] /= len_label
    average_unpopular["time_signature"] /= len_label

    print (average_popular["artist_popularity"])
    print (average_unpopular["artist_popularity"])
    print ("MASSIVE DUMP")
    pickle.dump(average_popular, open("../../../node/average_popular_features.p", "wb"))
    pickle.dump(average_unpopular, open("../../../node/average_unpopular_features.p", "wb"))

    print("Percent of training labels 1: ", count/len(training_labels))

    ############################################################

    ##### TRAIN THE MODEL ######################################
    # Initialize the corresponding type of the classifier
    # NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
    classifier1 = SVC(kernel="rbf", C=5, probability=True)
    classifier2 = SVC(kernel="rbf", C=5, probability=True)

    # TODO: Train your classifier using 'fit'
    classifier1.fit(training_features, training_labels)
    classifier2.fit(training_features2, training_labels2)

    ############################################################


    ###### VALIDATE THE MODEL ##################################
    # TODO: Print training mean accuracy using 'score'
    training_score1 = classifier1.score(training_features, training_labels)
    training_score2 = classifier2.score(training_features2, training_labels2)
  

    #print (classifier.coef_)

    print('training mean accuracy LogReg:', training_score1)
    print('training mean accuracy LogReg non binary:', training_score2)

    # TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
    print("Doing cross val now:")

    pickle.dump(classifier1, open("../../../node/binary_classifier2.p", "wb"))
    pickle.dump(classifier2, open("../../../node/nonbinary_classifier2.p", "wb"))
    predicted_probs = classifier2.predict(training_labels[0])
    print (predicted_probs)

    ############################################################


if __name__ == '__main__':
    main()

    # songs_features, songs_popularity = load_songs()

    # test_features, test_popularity = load_test_songs()
