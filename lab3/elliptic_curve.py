class EllipticCurve:
    def __init__(self, a, b):
        self.a = a
        self.b = b
        self.discriminant = -16 * (4 * a * a * a + 27 * b * b)

    def __str__(self):
        return "y^2 = x^3 + {0}x + {1}".format(str(self.a), str(self.b))


class Point:
    def __init__(self, curve, x, y, p):
        self.curve = curve
        self.x = x
        self.y = y
        self.p = p

    def __str__(self):
        return "({0}, {1}".format(self.x, self.y)

    def add(self, point2):
        x1, y1, x2, y2 = self.x, self.y, point2.x, point2.y
        if (x1, y1) == (x2, y2):
            lmbd = (3 * x1 * x1 + self.curve.a) / (2 * y1) % self.p
        else:
            lmbd = (y2 - y1)/(x2 - x1) % self.p

        x3 = (lmbd * lmbd - x1 - x2) % self.p
        y3 = (lmbd*(x1 - x3) - y1) % self.p

        return Point(self.curve, x3, -y3)





