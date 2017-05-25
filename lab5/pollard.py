from random import randint
from elliptic_curve import *


def H(X, L):
    return X.x % L


def pollard_method(E, P, Q, q, p):
    L = 32
    a = [None] * L
    b = [None] * L
    R = [None] * L

    for j in range(L):
        a[j] = randint(0, q-1)
        b[j] = randint(0, q-1)
        left_term = multiply(P, a[j], E.a, p)
        right_term = multiply(Q, b[j], E.a, p)
        R[j] = add(left_term, right_term, E.a, p)

    alpha = randint(0, q-1)
    beta = randint(0, q-1)
    left_term = multiply(P, alpha, E.a, p)
    right_term = multiply(Q, beta, E.a, p)
    T = add(left_term, right_term, E.a, p)
    T2 = T
    alpha2 = alpha
    beta2 = beta

    while True:
        j = H(T, L)
        T = add(T, R[j], E.a, p)
        alpha = (alpha + a[j]) % q
        beta = (beta + b[j]) % q

        for i in range(2):
            j = H(T2, L)
            T2 = add(T2, R[j], E.a, p)
            alpha2 = (alpha2 + a[j]) % q
            beta2 = (beta2 + b[j]) % q

        if T == T2:
            break

    if alpha == alpha2 and beta == beta2:
        raise ValueError('Choose another L!')

    d = (alpha - alpha2)*invert(beta2 - beta, q) % q
    return d


def main():
    # p = 2774052499
    # a = 2552774921
    # b = 1967537144
    # # d = 629204683
    # q = 924688404
    # Px = 2083077157
    # Py = 1745053455
    # Qx = 2508372582
    # Qy = 1108100667

    q = 167
    Px = 306
    Py = 304
    Qx = 146
    Qy = 65
    a = 1
    b = 11
    p = 307

    curve = EllipticCurve(a, b)
    P = Point(Px, Py)
    Q = Point(Qx, Qy)
    d = pollard_method(curve, P, Q, q, p)
    print('[+] Found d = {0}'.format(str(d))) if d else print('[-] Not found!')


main()




