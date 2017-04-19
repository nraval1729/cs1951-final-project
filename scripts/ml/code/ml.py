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
from sklearn.svm import LinearSVC
from tokenizer import Tokenizer

# # Load songs into two arrays and returns them (first array consists of
# # an array of tuples, where each tuple represents the features of a
# # particular song. second array consists of popularity for a song. indexing
# # matches for both arrays for each song).
def load_songs():
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../data/songs.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_popularity = []

    for song in c.execute('''
                    SELECT song_hotness, danceability, energy,
                    loudness, mode, tempo, key, mean_segment_timbre                  
                    FROM songs ORDER BY track_id LIMIT 1000
                '''):

        if (song[0] and not math.isnan(float(song[0]))):
            songs_features.append(tuple(float(f) for f in song[1:]))
            int_song = 0
            if (int( 100 * float(song[0])) < 60):
                int_song = 1
            songs_popularity.append(int_song)
    return songs_features, songs_popularity
# Same function as above, but loads the next 10 songs after the initial 1000 songs
# we trained on.
def load_test_songs():
    ### MODIFY THIS TO POINT TO YOUR DATABASE ###
    conn = sqlite3.connect('../../../data/database.db')
    conn.text_factory = str
    c = conn.cursor()

    songs_features = []
    songs_labels = []

    for song in c.execute('''
                    SELECT song_hotness, danceability, energy,
                    loudness, mode, tempo, key, mean_segment_timbre 
                    FROM songs ORDER BY track_id LIMIT 10 OFFSET 1000
                '''):

        if (song[0] and not math.isnan(float(song[0]))):  
            songs_features.append(tuple(float(f) for f in song[1:]))
            int_song = 0
            if (int( 100 * float(song[0])) > 60):
                int_song = 1
            songs_popularity.append(int_song)

    return songs_features, songs_popularity

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
    count = 0.0
    for label in training_labels:
        if label == 0:
            count += 1.0
    print("Percent of training labels 0: ", count/len(training_labels))

    ############################################################

    ##### TRAIN THE MODEL ######################################
    # Initialize the corresponding type of the classifier
    # NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
    classifier = LogisticRegression(C=0.5)

    # TODO: Train your classifier using 'fit'
    classifier.fit(training_features, training_labels)

    ############################################################


    ###### VALIDATE THE MODEL ##################################
    # TODO: Print training mean accuracy using 'score'
    training_score = classifier.score(training_features, training_labels)
    
    print('training mean accuracy:', training_score)

    # TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
    print("Doing cross val now:")
    scores = cross_val_score(classifier, training_features, training_labels, scoring='accuracy', cv=10)
    print("Done with cross val")

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
<<<<<<< HEAD:python/ml/code/ml.py
    (test_true_labels, test_texts) = load_test(opts.test)

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
=======
    (test_features, test_labels) = load_test_songs()
    print("Test_labesl: ", test_labels)

    # TODO: Predict the labels for the test set
    test_predicted_labels = classifier.predict(test_features)
    print("Predicted test labesl: ", test_predicted_labels)

    # TODO: Print mean test accuracy
    test_score = classifier.score(test_features, test_labels)

    print('predicted mean accuracy:', test_score)

        # TODO: Print the confusion matrix using your implementation
        # our_cm = our_confusion_matrix(test_true_labels, test_predicted_labels)
        # if (opts.p):
        #     print('our confusion matrix:')
        #     print(our_cm)

        # # TODO: Print the confusion matrix using sklearn's implementation
        # cm = confusion_matrix(test_true_labels, test_predicted_labels)
        # if (opts.p):
        #     print('sklearn confusion matrix:')
        #     print(cm)
>>>>>>> f59406a4b284a2c9cd60c50c2328948a19b07acd:scripts/ml/code/ml.py

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

    # songs_features, songs_popularity = load_songs()

    # test_features, test_popularity = load_test_songs()