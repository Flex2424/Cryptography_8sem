import argparse
from random import randint
from pygost import gost34112012256
from constants import *
from elliptic_curve import *
from gmpy2 import gcd
import asn1


curve = EllipticCurve(a, b)
P = Point(x, y)
Q = multiply(P, d, curve.a, p)


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


decoded_values = []


def parse_file(filename):
    with open(filename, 'rb') as file:
        data = file.read()
    file = asn1.Decoder()
    file.start(data)
    parsing_file(file)
    return


def parsing_file(file):
    while not file.eof():
        try:
            tag = file.peek()
            if tag.nr == asn1.Numbers.Null:
                break
            if tag.typ == asn1.Types.Primitive:
                tag, value = file.read()
                if tag.nr == asn1.Numbers.Integer:
                    decoded_values.append(value)
            else:
                file.enter()
                parsing_file(file)
                file.leave()
        except asn1.Error:
            break


def add_sign(data):
    hash = gost34112012256.new(data).digest()
    print('[+] Hash: {0}'.format(gost34112012256.new(data).hexdigest()))
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


def verify_sign(filename):
    parse_file('signature')

    s = decoded_values[-1]
    r = decoded_values[-2]
    q = decoded_values[-3]
    Q_x = decoded_values[0]
    Q_y = decoded_values[1]
    p = decoded_values[2]
    a = decoded_values[3]
    P_x = decoded_values[5]
    P_y = decoded_values[6]

    with open(filename, 'rb') as file:
        data = file.read()
    hash = gost34112012256.new(data).digest()
    e = int.from_bytes(hash, byteorder='big') % q
    if e == 0:
        e = 1

    v = invert(e, q)
    z_1 = s * v % q
    z_2 = -r * v % q
    tmp_1 = multiply(Point(P_x, P_y), z_1, a, p)
    tmp_2 = multiply(Point(Q_x, Q_y), z_2, a, p)
    C = add(tmp_1, tmp_2, a, p)
    R = C.x % q
    return True if R == r else False


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--sign", help="Add signature", action="store_true")
    parser.add_argument("--check", help="Check signature", action="store_true")
    parser.add_argument("--file", help="File")
    args = parser.parse_args()

    print('[+] a = {0}'.format(str(a)))
    print('[+] b = {0}'.format(str(b)))
    print('[+] p = {0}'.format(str(p)))
    print('[+] q = {0}'.format(str(q)))
    print('[+] x = {0}'.format(str(x)))
    print('[+] y = {0}'.format(str(y)))
    print()

    if args.sign:
        with open(args.file, 'rb') as file:
            data = file.read()
        print('[+] Success added signature') if add_sign(data) else print('[-] Wrong')

    if args.check:
        if verify_sign(args.file):
            print('[+] Sign is correct!')
        else:
            print('[-] Sign is incorrect!')


if __name__ == '__main__':
    main()







