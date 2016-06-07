import matplotlib.pyplot as plt
import itertools


def plot_digit(digit):

    fig=plt.figure()
    ax=fig.add_subplot(111)
    #all_data = [[1,10],[2,10],[3,10],[4,10],[5,10],[3,1],[3,2],[3,3],[3,4],[3,5]]
    #all_data = digit.curves[0]
    #plt.plot(*zip(*itertools.chain.from_iterable(itertools.combinations(all_data, 2))),color = 'brown', marker = 'o')


    for curve in digit.curves:
        x_points = []
        y_points = []
        for point in curve:
            x_points.append(point[0])
            y_points.append(point[1])

        plt.plot(x_points, y_points, linewidth = 2.0)

    plt.axis([0, 500, 0, 500])
    plt.show()
