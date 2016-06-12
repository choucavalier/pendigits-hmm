import math

class Digit:

    def __init__(self):
        self.curves = []
        self.label = -1

    def add_curve(self, points):
        self.curves.append(points)

    def set_label(self, label):
        self.label = int(label)

    def set_observations(self, observations):
        self.observations = observations

    def normalise(self):

        self.normalise_average()
        self.normalise_variance()

    def normalise_average(self):

        x_total = 0
        y_total = 0
        n = 0

        for curve in self.curves:
            for point in curve:
                x_total += point[0]
                y_total += point[1]
                n += 1

        x_avg = int(( float(x_total) / float(n) ))
        y_avg = int(( float(y_total) / float(n) ))

        for i in range(0, len(self.curves)):
            for j in range(0, len(self.curves[i])):
                self.curves[i][j][0] -= x_avg
                self.curves[i][j][1] -= y_avg


    # only call after normalising by average
    def normalise_variance(self):

        dx2_total = 0
        dy2_total = 0
        n = 0

        for curve in self.curves:
            for point in curve:
                dx2_total += point[0]*point[0]
                dy2_total += point[1]*point[1]
                n += 1

        x_var = float(dx2_total) / float(n)
        y_var = float(dy2_total) / float(n)

        x_stddev = math.sqrt(x_var)
        y_stddev = math.sqrt(y_var)

        for i in range(0, len(self.curves)):
            for j in range(0, len(self.curves[i])):

                x = float(self.curves[i][j][0]) / x_stddev
                y = float(self.curves[i][j][1]) / y_stddev
                self.curves[i][j] = [x, y]


    def __repr__(self):
        ret = "label : " + str(self.label) + "\n"

        n_points = 0
        for curve in self.curves:
            n_points += len(curve)

        ret += "Number of Curves : " + str(len(self.curves)) + " , Number of Points : " + str(n_points) + "\n"
        ret += str(self.curves)
        return ret
