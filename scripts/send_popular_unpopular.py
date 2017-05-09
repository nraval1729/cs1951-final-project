import pickle
import sys
import json
import os

cwd = os.getcwd()

def get_pickled_files():
	average_popular_features = pickle.load(open(cwd + "/../../node/average_popular_features.p", "rb"))

	average_unpopular_features = pickle.load(open(cwd + "/../../node/average_unpopular_features.p", "rb"))

	return (average_popular_features, average_unpopular_features)

def main():
	average_popular_features, average_unpopular_features = get_pickled_files()
	pop_unpop = {}
	pop_unpop["popular"] = average_popular_features
	pop_unpop["unpopular"] = average_unpopular_features

	print(json.dumps(pop_unpop))
	sys.stdout.flush()

if __name__ == "__main__":
	main()

