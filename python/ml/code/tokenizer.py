from porter_stemmer import PorterStemmer
import re
import string

stop = {' the ', ' is ', ' on ', ' a '}

class Tokenizer(object):
    def __init__(self):
        self.stemmer = PorterStemmer()

    # only admit non-number with length>2
    def qualify(self, word):
        return len(word)>2 and not word.isdigit()

    def process_tweet(self, tweet):
        # TODO: Change the text processing here
        # HINT: Refer to porter_stemmer_example.py to see how to use PorterStemmer

        #1
        tweet = tweet.lower()
        #10
        tweet = ''.join(ch for ch in tweet if ch not in stop)
        #4
        tweet = re.sub(r'\b\d\b', '', tweet)
        #6
        tweet = tweet.replace('#', '')
        #2
        tweet = self.stemmer.stem(tweet, 0,len(tweet)-1)
        #7
        tweet = re.sub(r'(https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9][a-zA-Z0-9-]+[a-zA-Z0-9]\.[^\s]{2,}|https?:\/\/(?:www\.|(?!www))[a-zA-Z0-9]\.[^\s]{2,}|www\.[a-zA-Z0-9]\.[^\s]{2,})', 'URL', tweet)
        #8
        tweet = re.sub(r'@[a-zA-Z0-9]+', 'ATUSER', tweet)
        #3
        exclude = set(string.punctuation)
        tweet = ''.join(ch for ch in tweet if ch not in exclude)
        #9
        tweet = re.sub(r'\b[0-9]+\w+', '', tweet)

        return tweet

    def __call__(self, tweet):
        # This function takes in a single tweet (just the text part)
        # then it will process/clean the tweet and return a list of tokens (words).
        # For example, if tweet was 'I eat', the function returns ['i', 'eat']

        # You will not need to call this function explictly.
        # Once you initialize your vectorizer with this tokenizer,
        # then 'vectorizer.fit_transform()' will implictly call this function to
        # extract features from the training set, which is a list of tweet texts.
        # So once you call 'fit_transform()', the '__call__' function will be applied
        # on each tweet text in the training set (a list of tweet texts),
        features = []
        for word in self.process_tweet(tweet).split():
            if self.qualify(word):
                # Stem
                word = self.stemmer.stem(word, 0, len(word) - 1)

                features.append(word)

        return features
