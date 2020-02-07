__author__           = "Dilawar Singh"
__copyright__        = "Copyright 2019-, Dilawar Singh"
__maintainer__       = "Dilawar Singh"
__email__            = "dilawars@ncbs.res.in"

import sys
import os
import random
import matplotlib.pyplot as plt
import itertools
import imageio
from pathlib import Path
import tifffile
import numpy as np

W_, H_ = 24, 24
summary_ = np.zeros((H_,W_))
frames_ = []
constraintWindowSize_ = 10

marginSize_ = 5

tempDir_ = Path('_figures')
tempDir_.mkdir(parents=True, exist_ok=True)

def showFrame(pixel, i, delay=1):
    global tempDir_
    import cv2
    global summary_, frames_
    mat = np.zeros_like(summary_)
    mat[pixel] = 1
    summary_ += mat
    extra = np.zeros_like(summary_)
    for f in frames_[-constraintWindowSize_:]:
        extra[f] = 1
    res = np.hstack((mat, summary_, extra))
    #final = cv2.resize(res, None, fx=5, fy=5,
    #    interpolation=cv2.INTER_CUBIC)
    cv2.imshow('window', res)
    cv2.waitKey(delay)
    imageio.imwrite(tempDir_ / f'{i:04d}.png', res)

def minDistance(f1, f2):
    # Both frames are guaranteed to have only 1 pixel.
    x1, y1 = f1
    x2, y2 = f2
    return ((x1-x2)**2 + (y1-y2)**2)**0.5

def genRandom():
    return random.randint(0, H_-1), random.randint(0, W_-1)

def main():
    global summary_, H_, W_, frames_
    Z = np.zeros_like(summary_)
    i, j = genRandom()
    allowedIndex = list(itertools.product(range(H_), range(W_)))
    random.shuffle(allowedIndex)

    iterWithoutChange = 0
    nGoodFrame = 0
    # Pick every 2nd frame.
    everyN = 2
    while allowedIndex and iterWithoutChange < 700:
        i, j = random.choice(allowedIndex)
        # If i is in top or bottom margin; ignore the pixel.
        if i < marginSize_ or i >= (H_ - marginSize_):
            allowedIndex.remove((i,j))
            continue
        badIndex = False
        for (x2,y2) in frames_[-constraintWindowSize_:]:
            d = minDistance((i, j), (x2,y2))
            if d < 2**0.5:
                print('☠', end=''); sys.stdout.flush()
                badIndex = True
                break

        if not badIndex:
            nGoodFrame += 1
            # Comment these lines out if every frame is needed.
            allowedIndex.remove((i,j))
            if nGoodFrame % everyN == 0:
                frames_.append((i,j))
                print(nGoodFrame, everyN)
                showFrame((i,j), nGoodFrame)
                iterWithoutChange = 0
            else:
                pass
        else:
            iterWithoutChange += 1

    # Write them to a tiff file.
    showFrame((i,j), nGoodFrame)
    outfile = 'single_pixel.tiff'
    with tifffile.TiffWriter(outfile, imagej=True) as tif:
        for i, j in frames_:
            frame = np.zeros_like(summary_)
            frame[i, j] = 255
            tif.save(np.uint8(frame))
    print( f"[INFO ] Saved to {outfile}" )


if __name__ == '__main__':
    main()
