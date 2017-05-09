from __future__ import division
import pickle
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


def get_pickled_files():
	average_popular_features = pickle.load(open("../../../node/average_popular_features.p", "rb"))

	average_unpopular_features = pickle.load(open("../../../node/average_unpopular_features.p", "rb"))

	return (average_popular_features, average_unpopular_features)

def main():
	average_popular_features, average_unpopular_features = get_pickled_files()

	print(average_popular_features)
	print(average_unpopular_features)
	sys.stdout.flush()

if __name__ == "__main__":
	main()

