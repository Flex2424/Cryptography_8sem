from random import randint
from pygost import gost34112012256
from constants import *
from elliptic_curve import *
from gmpy2 import gcd
import asn1


# Elliptic curve stuff
curve = EllipticCurve(a, b)     # curve itself
P = Point(x, y)                 # point P
Q = multiply(P, d, curve.a, p)  # public key


def generate_prime(q):
    while True:
        k = randint(1, q - 1)
        if gcd(k, q) == 1:
            return k


def encode_file_signature(Q, p, curve, P, q, r, s):
    struct = asn1.Encoder()
    struct.start()
    struct.enter(asn1.Numbers.Sequence)
    struct.enter(asn1.Numbers.Set)
    struct.enter(asn1.Numbers.Sequence)
    struct.write(b'\x00\x06\x07\x00', asn1.Numbers.OctetString)
    struct.write(b'gostSignKey', asn1.Numbers.UTF8String)
    struct.enter(asn1.Numbers.Sequence)
    struct.write(Q.x, asn1.Numbers.Integer)
    struct.write(Q.y, asn1.Numbers.Integer)
    struct.leave()

    struct.enter(asn1.Numbers.Sequence)
    struct.write(p, asn1.Numbers.Integer)
    struct.leave()

    struct.enter(asn1.Numbers.Sequence)
    struct.write(curve.a, asn1.Numbers.Integer)
    struct.write(curve.b, asn1.Numbers.Integer)
    struct.leave()

    struct.enter(asn1.Numbers.Sequence)
    struct.write(P.x, asn1.Numbers.Integer)
    struct.write(P.y, asn1.Numbers.Integer)
    struct.leave()
    struct.write(q, asn1.Numbers.Integer)
    struct.leave()

    struct.enter(asn1.Numbers.Sequence)
    struct.write(r, asn1.Numbers.Integer)
    struct.write(s, asn1.Numbers.Integer)
    struct.leave()
    struct.leave()

    struct.enter(asn1.Numbers.Sequence)
    struct.leave()
    struct.leave()

    return struct.output()


def add_sign(data):
    hash = gost34112012256.new(data).digest()
    int_hash = int.from_bytes(hash, byteorder='big')
    e = int_hash % q
    if e == 0:
        e = 1

    while True:
        k = generate_prime(q)
        C = multiply(P, k, curve.a, p)
        r = C.x % q
        if r == 0:
            continue

        s = (r*d + k*e) % q
        if s == 0:
            continue

        encoded_bytes = encode_file_signature(Q, p, curve, P, q, r, s)
        with open('signature', 'wb') as sign:
            sign.write(encoded_bytes)
        return True


def main():
    print('[+] a = {0}'.format(str(a)))
    print('[+] b = {0}'.format(str(b)))
    print('[+] p = {0}'.format(str(p)))
    print('[+] q = {0}'.format(str(q)))
    print('[+] x = {0}'.format(str(x)))
    print('[+] y = {0}'.format(str(y)))
    print()
    with open('/home/dima/pwned.txt', 'rb') as file:
        data = file.read()
    print('[+] Success added signature') if add_sign(data) else print('[-] Wrong')


if __name__ == '__main__':
    main()







