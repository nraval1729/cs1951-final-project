from __future__ import division
import sqlite3
import csv
import sys
import csv
import argparse
from collections import defaultdict
import util
import numpy
import json
import math
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics import confusion_matrix
from sklearn.model_selection import cross_val_score
from sklearn.naive_bayes import BernoulliNB
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC
from tokenizer import Tokenizer

cwd = os.getcwd()

def get_features_from_stdin():
	featureList = sys.stdin.readlines()
	print("THIS IS THE FEATURE JSON: ", featureList)

	return json.loads(lines[0])

def get_pickled_files():
	bc = pickle.load(open(cwd + "/../../node/binary_classifier.p", "rb"))

	nbc = pickle.load(open(cwd + "/../../node/nonbinary_classifier.p", "rb"))

	return (bc, nbc)

def get_predictions(bc, nbc):
	bc_unpickled = pickle.loads(bc)
	nbc_unpickled = pickle.loads(nbc)


def main():

	features_list = get_features_from_stdin()

	binary_classifier, nonbinary_classifier = get_pickled_files()
	
	predictions = get_predictions(binary_classifier, nonbinary_classifier)

if __name__ == "__main__":
	main()