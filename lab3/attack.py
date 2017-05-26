from random import randint
from math import log, gcd
from prime_base import PRIME_BASE
from collections import namedtuple
from gmpy2 import invert


Point = namedtuple("Point", "x y")
EllipticCurve = namedtuple("EllipticCurve", "a b")
Origin = None
tmp = 0


# Elliptic multiplication of point by number
def multiply(point, x, a, p):
    if x == 0:
        return None
    x_bin = [int(k) for k in bin(x)[2:]]
    result = Origin
    for k in x_bin:
        result = add(result, result, a, p)
        if k != 0:
            result = add(result, point, a, p)
    return result


# Elliption addition of points
def add(point_a, point_b, a, p):
    if point_a is Origin:
        return point_b
    elif point_b is Origin:
        return point_a

    s = slope(point_a, point_b, a, p)

    if s is None:
        return None
    else:
        s = int(s)
    x = (s ** 2 - point_a.x - point_b.x) % p
    y = (s * (point_a.x - x) - point_a.y) % p
    return Point(x, y)


# Elliptic slope
def slope(point_a, point_b, a, p):
    global tmp
    if point_a.x != point_b.x:
        tmp = point_b.x - point_a.x
        s = (point_b.y - point_a.y) * invert((point_b.x - point_a.x), p)
    elif point_a.y == point_b.y:
        tmp = 2 * point_a.y
        s = (3 * point_a.x ** 2 + a) * invert((2 * point_a.y), p)
    else:
        return None
    return s % p


def get_point(n):
    x = randint(1, n-1)
    y = randint(1, n-1)
    return Point(x, y)


def get_curve(n):
    while True:
        P = get_point(n)
        a = randint(1, n-1)
        b = (P.y**2 - P.x**3 - a*P.x) % n
        if 4*a**3 + 27*b**2 != 0:
            return EllipticCurve(a, b), P


def factorization(n, m):
    E, Q = get_curve(n)
    i = 0
    Q_i = Q
    while True:
        if i > m:
            factorization(n, m)
        else:
            i += 1
            alpha_i = int(0.5 * log(n) / log(PRIME_BASE[i]))
            j = 0
            if j > alpha_i:
                continue
            else:
                try:
                    Q_i = multiply(Q_i, PRIME_BASE[i], E.a, n)
                except ZeroDivisionError:
                    d = gcd(tmp, n)
                    if d != 1:
                        return gcd(tmp, n)
                    else:
                        break

                j += 1


def attack(e, n):
    d = 0
    while True:
        try:
            d = factorization(n, len(PRIME_BASE))
            if d:
                break
        except:
            pass

    p = d
    q = n / p
    phi_n = (p-1)*(q-1)
    print('[+] n = {0}'.format(str(n)))
    print('[+] p = {0}'.format(str(p)))
    print('[+] q = {0}'.format(str(q)))
    print('[+] phi_n = {0}'.format(str(phi_n)))
    private_key = invert(e, int(phi_n))
    print('[+] public_key = {0}'.format(str(e)))
    print('[+] private_key = {0}'.format(str(private_key)))


def main():
    n = 34737127653522095618245200797
    e = 65537
    # n = 9173503
    # e = 3
    attack(e, n)


if __name__ == '__main__':
    main()


