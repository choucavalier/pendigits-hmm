class Digit:

    def __init__(self):
        self.curves = []
        self.label = -1

    def add_curve(self, points):
        self.curves.append(points)

    def set_label(self, label):
        self.label = label

    def __repr__(self):
        ret = "label : " + str(self.label) + "\n"
        ret += "Number of Curves : " + str(len(self.curves)) + "\n"
        ret += str(self.curves)
        return ret
