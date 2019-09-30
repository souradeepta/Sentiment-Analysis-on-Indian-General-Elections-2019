
import pickle
from nltk.tokenize import word_tokenize
from textblob import TextBlob

from vote_classifier import get_instance

votes_classifier = get_instance()

word_features_file = open("pickles/word_features.pickle", "rb")
word_features = pickle.load(word_features_file)
word_features_file.close()

def find_features(document):
    words = word_tokenize(document)
    features = {}
    for w in word_features:
        features[w] = (w in words)
    return features

def sentiment(text):
    features = find_features(text)
    return votes_classifier.classify(features), votes_classifier.confidence(features)

def text_blob_sentiment(text):
    analysis = TextBlob(text)
    if analysis.sentiment[0]>0:
        #print()'Positive'
        return "pos"
    if analysis.sentiment[0]<0:
        #print 'Negative'
        return "neg"
    #print 'Neutral'
    return "neu"