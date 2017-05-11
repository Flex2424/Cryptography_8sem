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

    def __add__(self, point2):
        if self.curve != point2.curve:
            raise Exception("Can't add points on different curves!")
        if isinstance(point2, Ideal):
            return self

        x1, y1, x2, y2 = self.x, self.y, point2.x, point2.y
        if (x1, y1) == (x2, y2):
            if y1 == 0:
                return Ideal(self.curve, self.x, self.y, self.p)

            lmbd = (3 * x1 * x1 + self.curve.a) / (2 * y1) % self.p
        else:
            if x1 == x2:
                return Ideal(self.curve, self.x, self.y, self.p)

            lmbd = (y2 - y1)/(x2 - x1) % self.p

        x3 = (lmbd * lmbd - x1 - x2) % self.p
        y3 = (lmbd*(x1 - x3) - y1) % self.p

        return Point(self.curve, x3, -y3, self.p)

    def __sub__(self, Q):
        return self + -Q

    def __mul__(self, n):
        if not isinstance(n, int):
            raise Exception("Can't scale a point by something which isn't an int!")

        if n < 0:
            return -self * -n

        if n == 0:
            return Ideal(self.curve, self.x, self.y, self.p)

        Q = self
        R = self if n & 1 == 1 else Ideal(self.curve, self.x, self.y, self.p)

        i = 2
        while i <= n:
            Q += Q
            if n & i == i:
                R += Q
            i = i << 1
        return R

    def __rmul__(self, n):
        return self * n

    def __list__(self):
        return [self.x, self.y]

    def __eq__(self, other):
        if type(other) is Ideal:
            return False

        return self.x, self.y == other.x, other.y

    def __ne__(self, other):
        return not self == other

    def __getitem__(self, index):
        return [self.x, self.y][index]

    def __neg__(self):
        return Point(self.curve, self.x, -self.y, self.p)


class Ideal(Point):
    def __init__(self, curve, x, y, p):
        super().__init__(curve, x, y, p)
        self.curve = curve

    def __str__(self):
        return 'Ideal point'

    def __add__(self, Q):
        if self.curve != Q:
            raise Exception('Can not add points on different curves!')
        return Q

    def __mul__(self, n):
        if not isinstance(n, int):
            raise Exception("Can't scale a point by something which isn't an int!")
        else:
            return self

    def __neg__(self):
        return self

    def __eq__(self, other):
        return type(other) is Ideal






