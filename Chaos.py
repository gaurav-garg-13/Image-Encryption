import matplotlib.pyplot as plt
import cv2
import numpy as np
import random

def k():
    return round(random.uniform(3.67,3.99),6)

def keygen(x, r, size):
    key = []
    for i in range(size):
        x = r*x*(1-x)
        key.append(int((x*pow(10, 16)) % 256))

    return key


def subimage(img, r):
    h = img.shape[0]
    w = img.shape[1]
    z = 0
    key = keygen(0.01, r, h*w)
    enimg = np.zeros(shape=[h, w, 3], dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            enimg[i, j] = img[i, j] ^ key[z]  # pixel value xor with key value
            z += 1
    return enimg


def desubimage(enimg, r):
    h = enimg.shape[0]
    w = enimg.shape[1]
    z = 0
    key = keygen(0.01, r, h*w)
    decimg = np.zeros(shape=[h, w, 3], dtype=np.uint8)
    for i in range(h):
        for j in range(w):
            decimg[i, j] = enimg[i, j] ^ key[z]
            z += 1
    return decimg


def indexgen(x, r, n):
    index = []
    k = []
    for i in range(n):
        x = r*x*(1-x)
        k.append(x)
        index.append(i)
    # below the chaotic keys keys are arranget in ascending order which scrambles index positions
    for i in range(n):
        for j in range(n):
            if(k[i] > k[j]):
                k[i], k[j] = k[j], k[i]
                index[i], index[j] = index[j], index[i]
    return index


def shuffleimg(img, index, x, y):
    ecrimg = np.zeros(shape=[x, y, 3], dtype=np.uint8)
    for i in range(x):
        k = 0
        for j in range(y):
            try:
                ecrimg[i][j] = img[i][index[k]]
                k = k+1
            except:
                pass
    return ecrimg


def final_shuffle(img, r):
    h = img.shape[0]
    w = img.shape[1]
    ecrimg = np.zeros(shape=[h, w, 3], dtype=np.uint8)
    key = indexgen(0.1, r, w)
    ecrimg = shuffleimg(img, key, h, w)
    return ecrimg


def deshuffleimg(img, index, x, y):
    ecrimg = np.zeros(shape=[x, y, 3], dtype=np.uint8)
    for i in range(x):
        k = 0
        for j in range(y):
            try:
                ecrimg[i][index[k]] = img[i][j]
                k = k+1
            except:
                pass
    return ecrimg


def final_deshuffle(img, r):
    h = img.shape[0]
    w = img.shape[1]
    ecrimg = np.zeros(shape=[h, w], dtype=np.uint8)
    key = indexgen(0.1, r, w)
    ecrimg = deshuffleimg(img, key, h, w)
    return ecrimg


def encryption(img, r):
    eimg = final_shuffle(img, r)
    eimg = subimage(eimg, r)
    return eimg


def decryption(img, r):

    dimg = desubimage(img, r)
    dimg = final_deshuffle(dimg, r)
    return dimg
