__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import sys
import os
import random
import matplotlib.pyplot as plt
import itertools
import tifffile
import numpy as np

H_, W_ = 11, 8
res_ = np.zeros((H_,W_))
frames_ = []


def showFrame(mat, delay=1):
    import cv2
    global res_
    res_ += mat
    overlap = np.sum(frames_[-30:-1], axis=0)
    res = np.hstack((mat, res_, overlap))
    cv2.imshow('window', cv2.resize(res, None, fx=5, fy=5))
    cv2.waitKey(delay)

def minDistance(f1, f2):
    # Both frames are guaranteed to have only 1 pixel.
    x1, y1 = np.argwhere(f1>0)[0]
    x2, y2 = np.argwhere(f2>0)[0]
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
    

def main():
    global res_, H_, W_, frames_
    Z = np.zeros_like(res_)
    i = random.randint(0, H_-1)
    j = random.randint(0, W_-1)
    Z[i,j] = 1
    frames_ = [Z]
    while True:
        if res_.min() > 0:
            print("Whole space is covered")
            break
        # For how many frames it should not overlap. Continue with 2.
        Z = np.zeros_like(res_)
        i = random.randint(0, H_-1)
        j = random.randint(0, W_-1)
        Z[i, j] = 1
        badFrame = False
        for f in frames_[-30:-1]:
            d = minDistance(f, Z)
            if d < 2**0.5:
                print('☠', end=''); sys.stdout.flush()
                badFrame = True
                break

        if not badFrame:
            frames_.append(Z)
            showFrame(Z, 1)

    # Write them to a tiff file.
    outfile = 'single_pixel.tiff'
    with tifffile.TiffWriter(outfile, imagej=True) as tif:
        for frame in frames_:
            frame[frame==1] = 255
            tif.save(np.uint8(frame))
    print( f"[INFO ] Saved to {outfile}" )


if __name__ == '__main__':
    main()
