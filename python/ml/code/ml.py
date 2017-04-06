#!/usr/bin/env python3
import sqlite3
import csv
import sys
from __future__ import division
import sys
import csv
import argparse
from collections import defaultdict

import util

import numpy
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import LinearSVC
from tokenizer import Tokenizer

# # Load songs into two arrays and returns them (first array consists of
# # an array of tuples, where each tuple represents the features of a
# # particular song. second array consists of popularity for a song. indexing
# # matches for both arrays for each song).
def load_songs():
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../node/app/database.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_labels = []

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
        songs_labels.append(song[0])

    return songs_features, songs_labels

if __name__ == '__main__':
    songs_features, songs_labels = load_songs()

# See: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
# Source: http://www.goliatone.com/blog/2015/04/04/python-parse-boolean-values-with-argparse/
def str2bool(str):
  #susendberg's function
  return str.lower() in ("yes", "true", "t", "1")

def main():

    # Load training text and training labels
    training_features, training_labels = load_songs()

    # Transform training labels to numpy array (numpy.array)
    training_labels = numpy.array(training_labels)
    ############################################################

    ##### TRAIN THE MODEL ######################################
    # Initialize the corresponding type of the classifier
    # NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
    classifier = LogisticRegression()

    # TODO: Train your classifier using 'fit'
    classifier.fit(training_features, training_labels)

    ############################################################


    ###### VALIDATE THE MODEL ##################################
    # TODO: Print training mean accuracy using 'score'
    training_score = classifier.score(training_features, training_labels)
    
    print('training mean accuracy:', training_score)

    # TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
    scores = cross_val_score(classifier, training_features, training_labels, scoring='accuracy', cv=10)

    # TODO: Print the mean and std deviation of the cross validation score
    print('mean and std dev for cross validation scores:', scores.mean(), scores.std())

    ############################################################

    ##### EXAMINE THE MODEL ####################################
    # if opts.top is not None:
    #     # Print top n most informative features for positive and negative classes
    #     print('most informative features:')
    #     util.print_most_informative_features(opts.classifier, vectorizer, classifier, opts.top)
    ############################################################

    ##### TEST THE MODEL #######################################
    
        # Test the classifier on the given test set
        # TODO: Load test labels and texts using load_file()
        (test_true_labels, test_texts) = load_file(opts.test)

        # TODO: Extract test features using vectorizer.transform()
        test_features = vectorizer.transform(test_texts)

        # TODO: Predict the labels for the test set
        test_predicted_labels = classifier.predict(test_features)

        # TODO: Print mean test accuracy
        test_score = classifier.score(test_features, test_true_labels)
        if (opts.p):
            print('predicted mean accuracy:', test_score)

        # TODO: Print the confusion matrix using your implementation
        our_cm = our_confusion_matrix(test_true_labels, test_predicted_labels)
        if (opts.p):
            print('our confusion matrix:')
            print(our_cm)

        # TODO: Print the confusion matrix using sklearn's implementation
        cm = confusion_matrix(test_true_labels, test_predicted_labels)
        if (opts.p):
            print('sklearn confusion matrix:')
            print(cm)

    ############################################################

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

    songs_features, songs_popularity = load_songs()

    test_features, test_popularity = load_test_songs()
    print(test_popularity)
