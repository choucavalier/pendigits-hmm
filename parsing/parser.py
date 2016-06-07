from parsing import digit

class Parser:

    def __init__(self):
        pass

    def parse_file(self, filename):

        digits = []

        reading_digit = False
        buff = []
        with open(filename, 'r') as f:
            for line in f:

                line = line.rstrip()

                if line.startswith('.SEGMENT'):
                    reading_digit = True
                if line == '':
                    reading_digit = False

                if reading_digit:
                    buff.append(line)
                elif len(buff) > 0:
                    digits.append(self.parse_digit(buff))
                    buff = []

        return digits

    def parse_digit(self, lines):

        if len(lines) > 0 :
            dig = digit.Digit()

            started = False
            current_curve = []
            for line in lines:
                if line.startswith(' '):
                    points = line.split(' ')
                    current_curve.append((points[1], points[3]))
                elif line.startswith('.PEN_UP'):
                    dig.add_curve(current_curve)
                    current_curve = []
                elif line.startswith('.SEGMENT'):
                    split = line.split(' ')
                    dig.set_label(split[-1][1:-1])
            return dig

        else:
            return []
