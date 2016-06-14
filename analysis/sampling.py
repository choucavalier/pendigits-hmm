from analysis import training
from parsing import digit

import hmmlearn.hmm as hmm
import numpy as np

def get_samplings(hidden_markov_models, n_observation_classes, centroids, number_per_class, length):

    samplings = []

    for hidden_markov_model in hidden_markov_models:

        model_samplings = []

        for i in range(0, number_per_class):

            observation_sequence, state_sequence = sample_hidden_markov_model(hidden_markov_model.hidden_markov_model, length)
            observation_array = np.array(observation_sequence)

            sample_observations = hidden_markov_model.label_encoder.inverse_transform(observation_array)

            curves = []
            current_curve = []
            for observation in sample_observations:
                if observation < n_observation_classes - 2:
                    current_curve.append(centroids[observation])
                elif observation == n_observation_classes - 1: # pen up
                    if len(current_curve) > 0:
                        curves.append(current_curve)
                    current_curve = []
            if len(current_curve) > 0:
                curves.append(current_curve)

            dig = digit.Digit()
            for curve in curves:
                dig.add_curve(curve)

            model_samplings.append(dig)

        samplings.append(model_samplings)

    return samplings


def sample_hidden_markov_model(hidden_markov_model, length):

    state_sequence = []
    observation_sequence = []

    current_state = get_start_state(hidden_markov_model)
    current_observation = get_observation(hidden_markov_model, current_state)

    state_sequence.append(current_state)
    observation_sequence.append(current_observation)

    while len(state_sequence) < length:

        current_state = get_next_state(hidden_markov_model, current_state)
        current_observation = get_observation(hidden_markov_model, current_state)

        state_sequence.append(current_state)
        observation_sequence.append(current_observation)

    return (observation_sequence, state_sequence)


def get_start_state(hidden_markov_model):

    startprob = hidden_markov_model.startprob_

    val = np.random.ranf()
    counter = 0.0

    index = 0
    while index < len(startprob) and counter < val:
        counter += startprob[index]
        if index < len(startprob) and counter < val:
            index += 1

    return index


def get_observation(hidden_markov_model, state):

    emitmat = hidden_markov_model.emissionprob_

    val = np.random.ranf()
    counter = 0.0

    index = 0
    while index < len(emitmat[state]) and counter < val:
        counter += emitmat[state][index]
        if index < len(emitmat[state]) and counter < val:
            index += 1

    return index


def get_next_state(hidden_markov_model, state):

    transmat = hidden_markov_model.transmat_

    val = np.random.ranf()
    counter = 0.0

    index = 0
    while index < len(transmat[state]) and counter < val:
        counter += transmat[state][index]
        if index < len(transmat[state]) and counter < val:
            index += 1

    return index
