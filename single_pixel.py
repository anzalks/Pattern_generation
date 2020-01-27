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

W_, H_ = 20, 24
res_ = np.zeros((H_,W_))
frames_ = []
constraintWindowSize_ = 20

def showFrame(pixel, delay=1):
    import cv2
    global res_, frames_
    mat = np.zeros_like(res_)
    mat[pixel] = 1
    res_ += mat
    extra = np.zeros_like(res_)
    for f in frames_[-constraintWindowSize_:]:
        extra[f] = 1
    res = np.hstack((mat, res_, extra))
    cv2.imshow('window'
            , cv2.resize(res, None, fx=5, fy=5, interpolation=cv2.INTER_CUBIC)
            )
    cv2.waitKey(delay)

def minDistance(f1, f2):
    # Both frames are guaranteed to have only 1 pixel.
    x1, y1 = f1
    x2, y2 = f2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def genRandom():
    return random.randint(0, H_-1), random.randint(0, W_-1)

def main():
    global res_, H_, W_, frames_
    Z = np.zeros_like(res_)
    i, j = genRandom()
    allowedIndex = list(itertools.product(range(H_), range(W_)))
    random.shuffle(allowedIndex)
    i, j = allowedIndex.pop()
    frames_.append((i,j))
    while allowedIndex:
        i, j = random.choice(allowedIndex)
        badIndex = False
        for (x2,y2) in frames_[-constraintWindowSize_:]:
            d = minDistance((i, j), (x2,y2))
            if d < 2**0.5:
                print('xx', i, j, allowedIndex)
                print('☠', end=''); sys.stdout.flush()
                badIndex = True
                break

        if not badIndex:
            frames_.append((i,j))
            allowedIndex.remove((i,j))
            showFrame((i,j))
        print(len(allowedIndex))

    # Write them to a tiff file.
    outfile = 'single_pixel.tiff'
    with tifffile.TiffWriter(outfile, imagej=True) as tif:
        for i, j in frames_:
            frame = np.zeros_like(res_)
            frame[i, j] = 255
            tif.save(np.uint8(frame))
    print( f"[INFO ] Saved to {outfile}" )


if __name__ == '__main__':
    main()
