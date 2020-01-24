__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import sys
import os
import random
import matplotlib.pyplot as plt
import itertools
import numpy as np

def showFrame(mat, delay=500):
    import cv2
    cv2.imshow('frame', mat)
    cv2.waitKey(delay)

def main():
    H, W = 5, 4
    frames = []
    for i, j in itertools.product(range(H), range(W)):
        Z = np.zeros((H,W))
        #  frames.append(X)
        Z[i, j] = 1
        frames.append(Z)

    random.shuffle(frames)
    for f in frames:
        showFrame(f)


if __name__ == '__main__':
    main()
