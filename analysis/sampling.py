from analysis import training

import hmmlearn.hmm as hmm
import numpy as np

def get_samplings(hidden_markov_models, seed):

    samplings = []

    for hidden_markov_model in hidden_markov_models:

        sample_observations = hidden_markov_model.hidden_markov_model.sample(1, seed)

        print(sample_observations[0])

        processed_sample_observations = []
        for observation in sample_observations[0]:
            processed_sample_observations.append(observation[0])

        #print(processed_sample_observations)

        sample_observations = hidden_markov_model.label_encoder.inverse_transform(processed_sample_observations)
        #print(sample_observations[0])

    return samplings
