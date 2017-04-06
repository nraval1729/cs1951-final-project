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

def load_file(file_path):
    sentiments = []
    texts = []
    with open(file_path, 'r', encoding='latin1') as file_reader:
        reader = csv.reader(file_reader, delimiter=',', quotechar='"')
        for row in reader:
            sentiment = int(row[0])
            text = row[5]
            sentiments.append(sentiment)
            texts.append(text)
    return (sentiments, texts)

# See: https://stackoverflow.com/questions/15008758/parsing-boolean-values-with-argparse
# Source: http://www.goliatone.com/blog/2015/04/04/python-parse-boolean-values-with-argparse/
def str2bool(str):
  #susendberg's function
  return str.lower() in ("yes", "true", "t", "1")

def main():
    ##### DO NOT MODIFY THESE OPTIONS ##########################
    parser = argparse.ArgumentParser()
    parser.add_argument('-training', required=True, help='Path to training data')
    parser.add_argument('-test', help='Path to test data')
    parser.add_argument('-c', '--classifier', default='nb', help='nb | log | svm')
    parser.add_argument('-top', type=int, help='Number of top features to show')
    parser.add_argument('-p', type=str2bool, default='', help='If true, prints out information')
    opts = parser.parse_args()

    ############################################################
    # Note: anytime the print flag is set to '', you should not print anything out! this includes the placeholder print statements - either remove those or include them only when the print flag is set to true.

    ##### BUILD TRAINING SET ###################################
    # Initialize CountVectorizer
    # You will need to make a change in tokenizer.py
    tokenizer = Tokenizer()
    vectorizer = CountVectorizer(binary=True, lowercase=True, decode_error='replace', tokenizer=tokenizer)

    # Load training text and training labels
    (training_labels, training_texts) = load_file(opts.training)

    # Get training features using vectorizer
    training_features = vectorizer.fit_transform(training_texts)

    # Transform training labels to numpy array (numpy.array)
    training_labels = numpy.array(training_labels)
    ############################################################

    ##### TRAIN THE MODEL ######################################
    # Initialize the corresponding type of the classifier
    # NOTE: Be sure to name the variable for your classifier "classifier" so that our stencil works for you!
    if opts.classifier == 'nb':
        # TODO: Initialize Naive Bayes
        classifier = BernoulliNB(binarize=None)
    elif opts.classifier == 'log':
        # TODO: Initialize Logistic Regression
        classifier = LogisticRegression()
    elif opts.classifier == 'svm':
        # TODO: Initialize SVM
        classifier = LinearSVC()
    else:
        raise Exception('Unrecognized classifier!')

    # TODO: Train your classifier using 'fit'
    classifier.fit(training_features, training_labels)

    ############################################################


    ###### VALIDATE THE MODEL ##################################
    # TODO: Print training mean accuracy using 'score'
    training_score = classifier.score(training_features, training_labels)
    if (opts.p):
        print('training mean accuracy:', training_score)

    # TODO: Perform 10 fold cross validation (cross_val_score) with scoring='accuracy'
    scores = cross_val_score(classifier, training_features, training_labels, scoring='accuracy', cv=10)

    # TODO: Print the mean and std deviation of the cross validation score
    if (opts.p):
        print('mean and std dev for cross validation scores:', scores.mean(), scores.std())

    ############################################################

    ##### EXAMINE THE MODEL ####################################
    if opts.top is not None:
        # Print top n most informative features for positive and negative classes
        print('most informative features:')
        util.print_most_informative_features(opts.classifier, vectorizer, classifier, opts.top)
    ############################################################


    ##### TEST THE MODEL #######################################
    if opts.test is None:
        # Test the classifier on one sample test tweet
        # James Cameron 9:04 AM - 28 Jan 11
        test_tweet = 'ryan seacrest told me I had to get on Twitter.  So here I am.  First tweet.  I feel younger already.'
        # TODO: Extract features from the test tweet and transform them using vectorizer
        # HINT: vectorizer.transform() expects a list of tweets
        test_feature = vectorizer.transform([test_tweet])
        # test_feature = test_feature.reshape(1, -1)

        # TODO: Print the predicted label of the test tweet
        test_predicted_label = classifier.predict(test_feature)
        if (opts.p):
            print('predicted label for test tweet:')
            print(test_predicted_label)

        # TODO: Print the predicted probability of each label.
        if (opts.p):
            print('predicted probability for each label:')
            if opts.classifier != 'svm':
                # Use predict_proba
                print(classifier.predict_proba(test_feature))
            else:
                # Use decision_function
                print(classifier.decision_function(test_feature))

    else:
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
