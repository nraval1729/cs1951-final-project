from __future__ import division
import sqlite3
import csv
import sys
import csv
import argparse
from collections import defaultdict
import numpy
import json
import os
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
import pickle

cwd = os.getcwd()

def flush_output():
	sys.stdout.flush()

def get_features_from_stdin():
	line = sys.stdin.readline()
	feature_list = numpy.asarray([float(i) for i in json.loads(line)]).reshape(1,-1)
	# print(feature_list)
	# flush_output()

	return feature_list
	# return json.loads(line)

def get_pickled_files():
	bc = pickle.load(open(cwd + "/../../node/binary_classifier3.p", "rb"))

	nbc = pickle.load(open(cwd + "/../../node/nonbinary_classifier3.p", "rb"))

	return (bc, nbc)

def get_predictions(bc, nbc, fl):
	predictions = {}
	predictions["binary"] = str(bc.predict(fl)[0])
	predictions["non_binary"] = str(nbc.predict(fl)[0])
	# print(bc.predict(fl))
	# print(nbc.predict(fl))
	# flush_output()

	return predictions

def main():
	features_list = get_features_from_stdin()
 
	binary_classifier, nonbinary_classifier = get_pickled_files()
	
	predictions = get_predictions(binary_classifier, nonbinary_classifier, features_list)

	print(json.dumps(predictions))
	flush_output()

if __name__ == "__main__":
	main()