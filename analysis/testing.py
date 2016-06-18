from config import settings

import numpy as np
from ipywidgets import FloatProgress
from IPython.display import display
import pickle
import os.path

def evaluate_classification_accuracy(test_digits, predicted_labels):

    n_correct = 0
    n_false = 0

    i = 0
    for dig in test_digits:

        if dig.label == predicted_labels[i]:
            n_correct += 1
        else:
            n_false += 1

        i += 1

    return float(n_correct) / (float(n_correct) + float(n_false))

def predict_labels(test_digits, hidden_markov_models, centroids, n_observation_classes, n_hidden_states, n_iter, tol, display_progress):

    labels = []

    directory = settings.PREDICTED_LABELS_DIRECTORY + "centroids_" + str(n_observation_classes - 3)
    directory += "/hidden_states_" + str(n_hidden_states) + "/n_iter_" + str(n_iter) + "/tol_" + str(tol)
    filename = "predicted_digit_labels.dat"
    path = directory + "/" + filename
    if os.path.isfile(path):
        labels = pickle.load(open(path, 'rb'))
    else:

        f = FloatProgress(min=0, max=100)
        if display_progress:
            display(f)

        i = 0
        for dig in test_digits:
            label = predict_label(dig, hidden_markov_models, centroids, n_observation_classes)
            labels.append(label)
            f.value = (float(i) * 100.0) / float(len(test_digits))
            i += 1

        f.close()

        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(path,'wb') as f:
            pickle.dump(labels,f)

    return labels

def predict_label(test_digit, hidden_markov_models, centroids, n_observation_classes):

    max_score_value = 0
    max_score_label = 0
    max_score_set = False

    for hidden_markov_model in hidden_markov_models:

        score = get_hmm_probability(test_digit, hidden_markov_model, centroids, n_observation_classes)

        if not max_score_set or score > max_score_value:

            max_score_set = True
            max_score_value = score
            max_score_label = hidden_markov_model.digit_label

    return max_score_label


def get_hmm_probability(test_digit, hidden_markov_model, centroids,  n_observation_classes):

    pen_down_label = n_observation_classes - settings.PEN_DOWN_LABEL_DELTA
    pen_up_label = n_observation_classes - settings.PEN_UP_LABEL_DELTA
    stop_label = n_observation_classes - settings.STOP_LABEL_DELTA

    special_observations = [pen_down_label, pen_up_label, stop_label]
    train_digit_observations = [pen_down_label]

    for curve in test_digit.curves:
        for point in curve:

            min_dist_value = -1.0
            min_dist_obs = -1

            for obs in hidden_markov_model.digit_observations:

                if obs not in special_observations:

                    dx = centroids[obs][0] - point[0]
                    dy = centroids[obs][1] - point[1]

                    d2 = dx*dx + dy*dy

                    if min_dist_obs == -1 or d2 < min_dist_value:
                        min_dist_obs = obs
                        min_dist_value = d2

            train_digit_observations.append(min_dist_obs)
        train_digit_observations.append(pen_up_label)
    train_digit_observations.append(stop_label)

    encoded_train_digit_observations = []
    for obs in train_digit_observations:
        encoded_train_digit_observations.append(hidden_markov_model.label_encoder.transform(obs))

    X = np.array(encoded_train_digit_observations)
    lengths = [len(encoded_train_digit_observations)]

    score = hidden_markov_model.hidden_markov_model.score(np.atleast_2d(X).T, lengths)

    return score
