from parsing import parser, digit
from plotting import plotter
from analysis import training
from config import settings

import hmmlearn.hmm as hmm

import numpy as np

def main():

    test_plot_all_digits()
    #test_gaussian_hmm()
    #test_multinomial_hmm()

def test_plot_all_digits():

    parse = parser.Parser();
    #print("parsing digits")
    train_digits = parse.parse_file('data/pendigits-train');
    test_digits = parse.parse_file('data/pendigits-test')
    #print("finished parsing digits")

    #print("calculating centroids")
    centroids = training.get_digit_kmeans_centroids(train_digits, settings.N_OBSERVATION_CLASSES - 2)
    #print("finished calculating centroids")
    #print(centroids)

    training.set_digit_observations(train_digits, centroids)
    hidden_markov_models = training.train_hmm(train_digits)



def test_multinomial_hmm():

    X1 = [0, 2, 1, 1, 2, 0]
    X2 = [0, 3, 2]
    X = np.concatenate([X1, X2])
    lengths = [len(X1), len(X2)]

    print(X)
    X = np.atleast_2d(X).T

    hidden_markov_model = hmm.MultinomialHMM(n_components=3)
    hidden_markov_model.fit(X, lengths)



if __name__ == '__main__':

    main()
