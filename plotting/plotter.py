from config import settings

import matplotlib.pyplot as plt
import numpy as np
import itertools
from IPython.html.widgets import FloatProgress
from IPython.display import display


def plot_digit(digit, display_progress = False):

    fig=plt.figure()
    ax=fig.add_subplot(111)

    f = FloatProgress(min=0, max=100)
    if display_progress:
        display(f)

    n_points = 0
    for curve in digit.curves:
        n_points += len(curve)

    i = 0
    for curve in digit.curves:
        x_points = []
        y_points = []
        for point in curve:
            x_points.append(point[0])
            y_points.append(point[1])
            f.value = 100.0*(float(i) / float(n_points))
            i += 1

        plt.plot(x_points, y_points, linewidth = 2.0)
    f.close()

    plt.axis([settings.IMAGE_PLOT_X_MIN, settings.IMAGE_PLOT_X_MAX, settings.IMAGE_PLOT_Y_MIN, settings.IMAGE_PLOT_Y_MAX])
    plt.show()


def plot_digits_heatmap(digits, display_progress = False):

    f = FloatProgress(min=0, max=100)
    if display_progress:
        display(f)

    plt.clf();
    _, axarr = plt.subplots(2, 5);

    for i in range(0, 2):
        for j in range(0, 5):

            n = 5*i + j

            x_points = []
            y_points = []
            for digit in digits:
                if digit.label == n:
                    for curve in digit.curves:
                        for point in curve:
                            x_points.append(point[0])
                            y_points.append(point[1])

            heatmap, xedges, yedges = np.histogram2d(x_points, y_points, bins=50);

            extent = [xedges[0], xedges[-1], yedges[0], yedges[-1]];

            axarr[i, j].imshow(np.rot90(heatmap), extent=extent);
            #axarr[i, j].axis([settings.IMAGE_PLOT_X_MIN, settings.IMAGE_PLOT_X_MAX, settings.IMAGE_PLOT_Y_MIN, settings.IMAGE_PLOT_Y_MAX]);
            f.value += 10

    f.close()
    plt.show();
