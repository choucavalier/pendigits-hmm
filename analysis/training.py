from config import settings
from sklearn import preprocessing

from scipy.cluster.vq import vq, kmeans, whiten
import pickle
import os.path
import hmmlearn.hmm as hmm
import numpy as np


def get_digit_kmeans_centroids(digits, n_clusters):

    filename = settings.CENTROIDS_DIRECTORY + "centroids_" + str(n_clusters) + ".dat"
    if os.path.isfile(filename):
        centroids = pickle.load(open(filename, 'rb'))
        return centroids
    else:

        data = []
        for digit in digits:
            for curve in digit.curves:
                for point in curve:
                    data.append(point)

        centroids, _ = kmeans(data, n_clusters)

        with open(filename,'wb') as f:
            pickle.dump(centroids,f)

        return centroids


def set_digit_observations(digits, centroids, n_observation_classes):

    pen_down_label = n_observation_classes - settings.PEN_DOWN_LABEL_DELTA
    pen_up_label = n_observation_classes - settings.PEN_UP_LABEL_DELTA
    stop_label = n_observation_classes - settings.STOP_LABEL_DELTA

    for digit in digits:

        observations = []
        observations.append(pen_down_label)

        i = 0
        while i < len(digit.curves):

            curve = digit.curves[i]

            curve_data = []
            for point in curve:
                curve_data.append(point)
            idx,_ = vq(curve_data, centroids)
            for value in idx:
                observations.append(int(value))

            i += 1
            if i < len(digit.curves):
                observations.append(pen_up_label)
                observations.append(pen_down_label)

        observations.append(pen_up_label)
        observations.append(stop_label)
        digit.set_observations(observations)


def train_hmm(digits, n_observation_classes, n_hidden_states):

    hidden_markov_models = []

    for i in range(0, 10):

        digit_label = i + 1
        if digit_label == 10:
            digit_label = 0

        directory = settings.HIDDEN_MARKOV_MODE_DIRECTORY + "centroids_" + str(n_observation_classes - 3)
        directory += "/hidden_states_" + str(n_hidden_states)
        filename = "digit_label_" + str(digit_label) + ".dat"
        path = directory + "/" + filename
        if os.path.isfile(path):
            hidden_markov_model = pickle.load(open(path, 'rb'))
            hidden_markov_models.append(hidden_markov_model)
        else:

            digit_observations = []
            for dig in digits:
                if dig.label == digit_label:
                    for observation in dig.observations:
                        if not observation in digit_observations:
                            digit_observations.append(observation)

            transmat = initialise_random_transition_matrix(n_hidden_states)
            emitmat = initialise_random_emission_matrix(n_hidden_states, len(digit_observations))
            startprob = initialise_random_start_probability_matrix(n_hidden_states)

            h = hmm.MultinomialHMM(n_components=n_hidden_states, verbose=settings.HIDDEN_MARKOV_MODEL_VERBOSE, n_iter = settings.HIDDEN_MARKOV_MODEL_N_ITER)
            h.startprob_ = startprob
            h.transmat_ = transmat
            h.emissionprob_ = emitmat

            samples = []
            lengths = []
            for dig in digits:
                if dig.label == digit_label:
                    samples += dig.observations
                    lengths.append(len(dig.observations))

            le = preprocessing.LabelEncoder()
            X = np.array(samples)
            X = le.fit_transform(X)
            h.fit(np.atleast_2d(X).T, lengths)

            hidden_markov_model = HiddenMarkovModel(h, le, digit_label, digit_observations)
            hidden_markov_models.append(hidden_markov_model)

            if not os.path.exists(directory):
                os.makedirs(directory)
            with open(path,'wb') as f:
                pickle.dump(hidden_markov_model,f)

    return hidden_markov_models

class HiddenMarkovModel():

    def __init__(self, multinomialHMM, label_encoder, digit_label, digit_observations):

        self.hidden_markov_model = multinomialHMM
        self.label_encoder = label_encoder
        self.digit_label = digit_label
        self.digit_observations = digit_observations

def initialise_random_transition_matrix(n_hidden_states):

    transmat = np.random.rand(n_hidden_states, n_hidden_states)
    row_sums = transmat.sum(axis=1)
    return transmat / row_sums[:, np.newaxis]

def initialise_random_emission_matrix(n_hidden_states, n_observation_classes):

    emitmat = np.random.rand(n_hidden_states, n_observation_classes)
    row_sums = emitmat.sum(axis=1)
    return emitmat / row_sums[:, np.newaxis]

def initialise_random_start_probability_matrix(n_hidden_states):

    startprob = np.random.rand(1, n_hidden_states)
    row_sums = startprob.sum(axis=1)
    return startprob / row_sums[:, np.newaxis]



def initialise_better_matrices(n_hidden_states, digit_observations):

    transmat = np.zeros(n_hidden_states, n_hidden_states)
    emitmat = np.zeros(n_hidden_states, n_observation_classes)
    startprob = np.zeros(1, n_hidden_states)



    return transmat, emitmat, startprob
