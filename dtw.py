import operator
import pickle
from collections import defaultdict

import numpy as np
from scipy.spatial.distance import euclidean

from speech_dtw import _dtw

def main():

    with open('train_sequences', 'rb') as f:
        train_sequences = pickle.load(f)
    with open('test_sequences', 'rb') as f:
        test_sequences = pickle.load(f)
    with open('test_expected_labels', 'rb') as f:
        test_expected_labels = pickle.load(f)


    for i, x_test in enumerate(test_sequences):
        test_sequences[i] = np.asarray(
            np.array([list(x_test)], dtype=np.double).T, order='c')

    for label in train_sequences.keys():
        for i, x_train in enumerate(train_sequences[label]):
            train_sequences[label][i] = np.asarray(
                np.array([list(x_train)], dtype=np.double).T, order='c')

    test_predicted_labels = np.ndarray(shape=(len(test_sequences),))

    for i, x_test in enumerate(test_sequences):
        costs = defaultdict(int)
        for label in train_sequences.keys():
            for x_train in train_sequences[label]:
                path, cost = _dtw.multivariate_dtw(x_test, x_train,
                                                   metric='euclidean')
                costs[label] += cost
            costs[label] /= len(train_sequences[label]) # normalize
        predicted_label = min(costs.keys(), key=(lambda k: costs[k]))
        test_predicted_labels[i] = predicted_label
        print('{}/{}'.format(i, len(test_sequences)),
              test_expected_labels[i], test_predicted_labels[i])

    with open('labels.dat', 'wb') as f: pickle.dump(test_predicted_labels, f)

if __name__ == '__main__':
    main()
