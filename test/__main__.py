from parsing import parser, digit
from plotting import plotter
from analysis import training
from config import settings

def main():

    test_plot_all_digits()


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


if __name__ == '__main__':

    main()
