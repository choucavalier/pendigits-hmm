from config import settings

from scipy.cluster.vq import vq, kmeans, whiten
import pickle
import os.path
import hmmlearn.hmm as hmm
import numpy as np

def get_digit_kmeans_centroids(digits, n_clusters):

    if os.path.isfile(settings.CENTROIDS_FILENAME):
        centroids = pickle.load(open(settings.CENTROIDS_FILENAME, 'rb'))
        return centroids
    else:

        data = []
        for digit in digits:
            for curve in digit.curves:
                for point in curve:
                    data.append(point)

        centroids, _ = kmeans(data, n_clusters)

        with open(settings.CENTROIDS_FILENAME,'wb') as f:
            pickle.dump(centroids,f)

        return centroids


def set_digit_observations(digits, centroids):


    for digit in digits:

        observations = []
        observations.append(254) # pen down

        i = 0
        while i < len(digit.curves):

            curve = digit.curves[i]

            curve_data = []
            for point in curve:
                curve_data.append(point)
            idx,_ = vq(curve_data, centroids)
            for value in idx:
                observations.append(value)

            i += 1
            if i < len(digit.curves):
                observations.append(255) # pen up
                observations.append(254) # pen down

        observations.append(255) # pen up
        digit.set_observations(observations)

def train_hmm(digits):

    hidden_markov_models = []

    for i in range(0, 10):

        label = i + 1
        if label == 10:
            label = 0

        transmat = initialise_random_transition_matrix()
        emitmat = initialise_random_emission_matrix()
        startprob = initialise_random_start_probability_matrix()


    return hidden_markov_models

def initialise_random_transition_matrix():

    transmat = np.random.rand(settings.N_HIDDEN_MARKOV_MODEL_STATES, settings.N_HIDDEN_MARKOV_MODEL_STATES)
    row_sums = transmat.sum(axis=1)
    return transmat / row_sums[:, np.newaxis]

def initialise_random_emission_matrix():

    emitmat = np.random.rand(settings.N_HIDDEN_MARKOV_MODEL_STATES, settings.N_OBSERVATION_CLASSES)
    row_sums = emitmat.sum(axis=1)
    return emitmat / row_sums[:, np.newaxis]

def initialise_random_start_probability_matrix():

    startprob = np.random.rand(1, settings.N_HIDDEN_MARKOV_MODEL_STATES)
    row_sums = startprob.sum(axis=1)
    return startprob / row_sums[:, np.newaxis]
