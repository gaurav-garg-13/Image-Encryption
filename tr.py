import matplotlib.pyplot as plt
import cv2
import numpy as np
from random import randrange, getrandbits


def power(a, d, n):
    ans = 1
    while d != 0:
        if d % 2 == 1:
            ans = ((ans % n)*(a % n)) % n
        a = ((a % n)*(a % n)) % n
        d >>= 1
    return ans


def MillerRabin(N, d):
    a = randrange(2, N - 1)
    x = power(a, d, N)
    if x == 1 or x == N-1:
        return True
    else:
        while(d != N-1):
            x = ((x % N)*(x % N)) % N
            if x == 1:
                return False
            if x == N-1:
                return True
            d <<= 1
        return False


def is_prime(N, K):
    if N == 3 or N == 2:
        return True
    if N <= 1 or N % 2 == 0:
        return False
    d = N-1
    while d % 2 != 0:
        d /= 2
    for _ in range(K):
        if not MillerRabin(N, d):
            return False
    return True


def generate_prime_candidate(length):
    p = getrandbits(length)
    p |= (1 << length - 1) | 1
    return p


def generatePrimeNumber(length):
    A = 4
    while not is_prime(A, 128):
        A = generate_prime_candidate(length)
    return A


def gcdExtended(E, eulerTotient):
    a1, a2, b1, b2, d1, d2 = 1, 0, 0, 1, eulerTotient, E

    while d2 != 1:
        k = (d1//d2)

        temp = a2
        a2 = a1-(a2*k)
        a1 = temp

        temp = b2
        b2 = b1-(b2*k)
        b1 = temp

        temp = d2
        d2 = d1-(d2*k)
        d1 = temp

        D = b2

    if D > eulerTotient:
        D = D % eulerTotient
    elif D < 0:
        D = D+eulerTotient
    return D


def mod_inverse(x, y):

    # See: http://en.wikipedia.org/wiki/Extended_Euclidean_algorithm
    def eea(a, b):
        if b == 0:
            return (1, 0)
        (q, r) = (a//b, a % b)
        (s, t) = eea(b, r)
        return (t, s-(q*t))

    inv = eea(x, y)[0]
    if inv < 1:
        inv += y  # we only want positive values
    return inv


def keys(length=4):
    P = generatePrimeNumber(length)
    Q = generatePrimeNumber(length)

    N = P*Q
    eT = (P-1) * (Q-1)
    e = 3
    while eT % e == 0 or e % 2 == 0:
        e += 1

    d = mod_inverse(e, eT)
    return eT, e, N, d


def p(m, e, N):
    f = (m**e) % N
    return f


def encrypt(img, e, N):
    row, col = img.shape[0], img.shape[1]
    for i in range(0, row):
        for j in range(0, col):
            r, g, b = img[i, j]
            C1 = p(r, e, N)
            C2 = p(g, e, N)
            C3 = p(b, e, N)
            #C1 = C1 % 256
            #C2 = C2 % 256
            #C3 = C3 % 256
            img[i, j] = [C1, C2, C3]
    return img


def decrypt(img, D, N):
    row, col = img.shape[0], img.shape[1]
    for i in range(0, row):
        for j in range(0, col):
            r, g, b = img[i, j]
            M1 = p(r, D, N)
            M2 = p(g, D, N)
            M3 = p(b, D, N)
            img[i, j] = [M1, M2, M3]
    return img
