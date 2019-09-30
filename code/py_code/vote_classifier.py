
import pickle
from nltk.classify import ClassifierI
from statistics import mode

class VoteClassifier(ClassifierI):
    def __init__(self, *classifiers):
        self._classifers = classifiers

    def classify(self, features):
        votes = []
        for c in self._classifers:
            v = c.classify(features)
            votes.append(v)
        return mode(votes)

    def confidence(self, features):
        votes = []
        for c in self._classifers:
            v = c.classify(features)
            votes.append(v)

        choice_votes = votes.count(mode(votes))
        confidence_factor = choice_votes / len(votes)

        return confidence_factor

def get_instance():
    file = open("pickles/Naive_Bayes.pickle", "rb")
    NB_classifier = pickle.load(file)
    file.close()

    file = open("pickles/Multinomial_NB.pickle", "rb")
    MNB_classifier = pickle.load(file)
    file.close()

    file = open("pickles/Bernoulli_NB.pickle", "rb")
    BernoulliNB_classifier = pickle.load(file)
    file.close()

    file = open("pickles/Logistic_Regression.pickle", "rb")
    LogisticRegression_classifier = pickle.load(file)
    file.close()

    file = open("pickles/Linear_SVC.pickle", "rb")
    LinearSVC_classifier = pickle.load(file)
    file.close()

    return VoteClassifier(NB_classifier, MNB_classifier, BernoulliNB_classifier, LogisticRegression_classifier, LinearSVC_classifier)