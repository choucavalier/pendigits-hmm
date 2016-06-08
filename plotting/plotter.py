from config import settings

import matplotlib.pyplot as plt
import itertools


def plot_digit(digit):

    fig=plt.figure()
    ax=fig.add_subplot(111)

    for curve in digit.curves:
        x_points = []
        y_points = []
        for point in curve:
            x_points.append(point[0])
            y_points.append(point[1])

        plt.plot(x_points, y_points, linewidth = 2.0)

    plt.axis([settings.IMAGE_PLOT_X_MIN, settings.IMAGE_PLOT_X_MAX, settings.IMAGE_PLOT_Y_MIN, settings.IMAGE_PLOT_Y_MAX])
    plt.show()
