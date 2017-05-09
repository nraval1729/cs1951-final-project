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
        query += " artist_hotness, artist_familiarity"

    query += " tempo, key, tempo * mode, mode, mean_segment_timbre, mean_segment_pitch FROM songs ORDER BY track_id"

    return query

# # Load songs into two arrays and returns them (first array consists of
# # an array of tuples, where each tuple represents the features of a
# # particular song. second array consists of popularity for a song. indexing
# # matches for both arrays for each song).
def load_songs(useGenre, useDance, useEnergy, useLoudness, useArtist, training):
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../data/songs.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_popularity = []

    query = choose_query(useGenre, useDance, useEnergy, useLoudness, useArtist)

    if training:
        query += " LIMIT 2000"
    else:
        query += " LIMIT 500 OFFSET 2000"

    for song in c.execute(query):
        #print (song)
        if (song[0] and not math.isnan(float(song[0]))):
           

            #GENRE Features
            if (useGenre):
                features = list(float(f) for f in song[2:])
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
            if (int( 100 * float(song[0])) > 55.0):
                int_song = 1
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
    songs_features, songs_labels = load_songs(False, False, False, True, True, True)

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
    training_features, training_labels = load_songs(False, False, False, True, True, True)
    count = 0.0
    for label in training_labels:
        if label == 1:
            count += 1.0
    print("Percent of training labels 1: ", count/len(training_labels))

    ############################################################

    ##### TRAIN THE MODEL ######################################
    # Initialize the corresponding type of the classifier
    # NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
    classifier1 = LogisticRegression()
    classifier2 = SVC(kernel='linear')
    classifier3 = SVC(kernel='rbf')

    # TODO: Train your classifier using 'fit'
    classifier1.fit(training_features, training_labels)
    classifier2.fit(training_features, training_labels)
    classifier3.fit(training_features, training_labels)

    ############################################################


    ###### VALIDATE THE MODEL ##################################
    # TODO: Print training mean accuracy using 'score'
    training_score1 = classifier1.score(training_features, training_labels)
    training_score2 = classifier2.score(training_features, training_labels)
    training_score3 = classifier3.score(training_features, training_labels)
    #predicted_probs = classifier.predict_proba(training_labels)

    #print (classifier.coef_)
    #print (predicted_probs)

    print('training mean accuracy LogReg:', training_score1)
    print('training mean accuracy linear SVM:', training_score2)
    print('training mean accuracy gaussian SVM:', training_score3)

    # TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
    print("Doing cross val now:")
    scores1 = cross_val_score(classifier1, training_features, training_labels, scoring='accuracy', cv=10)
    scores2 = cross_val_score(classifier2, training_features, training_labels, scoring='accuracy', cv=10)
    scores3 = cross_val_score(classifier3, training_features, training_labels, scoring='accuracy', cv=10)
    print("Done with cross val")

    # TODO: Print the mean and std deviation of the cross validation score
    print('mean and std dev for cross validation scores for LogReg:', scores1.mean(), scores1.std())
    print('mean and std dev for cross validation scores for linear SVM:', scores2.mean(), scores2.std())
    print('mean and std dev for cross validation scores for gaussian SVM:', scores3.mean(), scores3.std())

    print(classifier1.coef_)

    ############################################################

    (test_features, test_labels) = load_songs(False, False, False, True, True, False)

    pred_labels1 = classifier1.predict(test_features)
    pred_labels2 = classifier2.predict(test_features)
    pred_labels3 = classifier3.predict(test_features)

    print('predicted mean accuracy LogReg: ' + str(classifier1.score(test_features, test_labels)))
    print('predicted mean accuracy linear SVM: ' + str(classifier2.score(test_features, test_labels)))
    print('predicted mean accuracy gaussian SVM: ' + str(classifier3.score(test_features, test_labels)))

    confusion1 = our_confusion_matrix(test_labels, pred_labels1)
    confusion2 = our_confusion_matrix(test_labels, pred_labels2)
    confusion3 = our_confusion_matrix(test_labels, pred_labels3)

    print('confusion matrix for LogReg: ' + str(confusion1))
    print('confusion matrix for linear SVM: ' + str(confusion2))
    print('confusion matrix for gaussian SVM: ' + str(confusion3))

def our_confusion_matrix(true, pred):
    our_confusion_matrix = [[0, 0],
                            [0, 0]]

    for i in range(0, len(true)):
        if (true[i] == pred[i]):
            if (pred[i]):
                our_confusion_matrix[0][0] += 1
            else:
                our_confusion_matrix[1][1] += 1
        else:
            if (pred[i]):
                our_confusion_matrix[1][0] += 1
            else:
                our_confusion_matrix[0][1] += 1

    return numpy.array(our_confusion_matrix)

if __name__ == '__main__':   
    main()

    # songs_features, songs_popularity = load_songs()

    # test_features, test_popularity = load_test_songs()