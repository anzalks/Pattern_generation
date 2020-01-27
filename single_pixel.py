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

H_, W_ = 20, 24
res_ = np.zeros((H_,W_))


def showFrame(pixel, delay=1):
    import cv2
    global res_
    i, j = pixel
    mat = np.zeros_like(res_)
    mat[i, j] = 1
    res_ += mat
    res = np.hstack((mat, res_))
    cv2.imshow('window', cv2.resize(res, None, fx=5, fy=5))
    cv2.waitKey(delay)

def minDistance(f1, f2):
    # Both frames are guaranteed to have only 1 pixel.
    x1, y1 = f1
    x2, y2 = f2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5
    

def main():
    global res_, H_, W_ Z = np.zeros_like(res_) i = random.randint(0, H_-1)
    j = random.randint(0, W_-1) frames = [(i,j)] while True:
        if res_.min() > 0:
            print("Whole space is covered") break
        #  frames.append(X) # For how many frames it should not
        overlap. Continue with 2.  i = random.randint(0, H_-1) j =
        random.randint(0, W_-1) if (i, j) in frames:
            print(end='.')  continue
        badIndex = False for (x2,y2) in frames[-20:-1]:
            d = minDistance((i, j), (x2,y2)) if d < 2**0.5:
                print('☠', end=''); sys.stdout.flush() badIndex = True break

        if not badIndex:
            frames.append((i,j))
            showFrame((i,j), 1)

    # Write them to a tiff file.
    outfile = 'single_pixel.tiff'
    with tifffile.TiffWriter(outfile, imagej=True) as tif:
        for i, j in frames:
            frame = np.zeros_like(res_)
            frame[i, j] = 255
            tif.save(np.uint8(frame))
    print( f"[INFO ] Saved to {outfile}" )


if __name__ == '__main__':
    main()
