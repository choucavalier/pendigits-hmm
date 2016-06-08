from parsing import parser, digit
from plotting import plotter

def main():

    test_plot_all_digits()


def test_plot_all_digits():

    parse = parser.Parser();
    train_digits = parse.parse_file('data/pendigits-train');
    test_digits = parse.parse_file('data/pendigits-test')

    #plotter.plot_digit(train_digits[20])
    plotter.plot_all_digit_points(train_digits)


if __name__ == '__main__':

    main()
