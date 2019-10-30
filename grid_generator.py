#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Oct 23 13:23:35 2019

@author: anzal
"""

import random
import numpy as np
from pathlib import Path
import random
import matplotlib.pyplot as plt
import imageio
import tifffile

class Args: pass 
args_ = Args()

def distance(p1, p2):
    x0, y0 = p1
    x1, y1 = p2
    return ((x1-x0)**2 + (y1-y0)**2)**0.5

def saveFrame(img, outfile):
    imageio.imwrite(outfile, img)

def showFrame(img, delay=20):
    import cv2
    cv2.imshow('FRAME', img)
    cv2.waitKey(delay)
    return

def isGapConditionFullfilled(p, ps, gap):
    x, y = p
    for pp in ps:
        d = distance(p, pp)
        if int(d) <= gap:
            return False
    return True

def create_pattern(W, H, nBright, gap, fixed=[]):
    img = np.zeros(shape=(W, H))
    brightIndices = fixed[:]
    status = True
    R, C = np.arange(img.shape[0]), np.arange(img.shape[1])
    if not gap:
        gap = -1
    nIter = 0
    while len(brightIndices) < nBright:
        x, y = random.choice(R), random.choice(C)
        nIter += 1
        if isGapConditionFullfilled((x,y), brightIndices, gap):
            brightIndices.append((x,y))
        if nIter > 100:
            print(end='💀')
            status = False
            break
    for x, y in brightIndices:
        img[x, y] = 1
    return img, status

def overlap(imgA, imgB):
    f = imgA + imgB
    return len(np.where(f==f.max())[0])

def generateFixedBrightPixels(n, gap, W, H):
    if n == 0:
        return []
    a, b = random.randrange(0, W), random.randrange(0,H)
    fixed = [(a,b)]
    while len(fixed) < n:
        p1 = random.randrange(0, W), random.randrange(0,H)
        good = True
        for p2 in fixed:
            if int(distance(p1,p2)) <= gap:
                good = False
        if good:
            fixed.append(p1)
    return fixed


def main(**kwargs):
    outdir = Path()/'frames'
    outdir.mkdir(exist_ok=True, parents=True)

    W, H = kwargs['width'], kwargs['height']
    nBright = kwargs['num_brights']
    nFixedBright = kwargs['num_fixed_brights']
    gap = kwargs['gap']
    print(f"[INFO] width {W}, height {H}. nBright {nBright}. gap {gap}")
    allpats = []
    nIter = 0
    fixed = generateFixedBrightPixels(nFixedBright, gap, W, H)
    while len(allpats) < kwargs['num_patterns']:
        img, success = create_pattern(W, H, nBright, gap, fixed)
        if success:
            #  saveFrame(img, outdir/f'f{nIter:05d}.png')
            showFrame(img, 10)
            allpats.append(img)
            nIter += 1
        if nIter > 10 * kwargs['num_patterns']:
            print( f"[WARN ] Too many iteration. Giving up." )
            break


    # Generate a figure for statistics.
    plt.figure(figsize=(8, 3))
    ax1 = plt.subplot(121)
    ax1.set_title('AVG: mean of all frames')
    avg = np.mean(allpats, axis=0)

    toPlot = avg.copy()
    toPlot[toPlot==0] = np.nan
    im = ax1.imshow(toPlot, aspect='auto', interpolation='none'
            , vmax=np.mean(avg)+2*np.std(avg)
            , cmap='rainbow'
            )
    plt.colorbar(im, ax=ax1)

    ax2 = plt.subplot(122)
    ax2.hist(np.ravel(avg), bins=np.linspace(0, 1.0, 2*len(allpats)))
    ax2.set_xlabel('pixel values in AVG mat')

    coverage = 100*(1-len(np.where(avg == 0)[0])/W/H)
    plt.suptitle(f'Coverage percentage {coverage:.1f}%, N={len(allpats)}')
    plt.tight_layout(rect=(0, 0, 1, 0.95))

    outfile = kwargs['outfile']
    plt.savefig(f'{outfile}.png')

    # final save
    with tifffile.TiffWriter(outfile, imagej=True) as tif:
        for frame in allpats:
            frame[frame==1] = 255
            tif.save(np.uint8(frame))
    print( f"[INFO ] Saved to {outfile}" )

if __name__ == '__main__':
    import argparse
    # Argument parser.
    description = '''Pattern Generator for Polygon.'''
    parser = argparse.ArgumentParser(description=description)
    parser.add_argument('--width', '-W'
            , required = False, default = 5, type=int
            , help = 'WIDTH of pattern'
            )
    parser.add_argument('--height', '-H'
            , required = False, default=7, type=int
            , help = 'WIDTH of the pattern'
            )
    parser.add_argument('--num-fixed-brights', '-nFB'
             , required=False, type=int, default=0
             , help = 'How many bright pixels must have fixed position.'
             )
    parser.add_argument('--magnification', '-m'
             , required = False, default = 40
             , help = 'Magnification of objective lens.'
             )
    parser.add_argument('--num-brights', '-nB'
             , required = False, default=5, type=int
             , help = 'Number of bright pixels)'
             )
    parser.add_argument('--gap', '-g'
             , required = False, type=int, default=2
             , help = 'Gap between nearest bright neighbours. <=0 removes '
                      ' restriction.'
             )
    parser.add_argument('--num-patterns', '-N'
             , required = False, default = 10, type=int
             , help = 'Number of patterns to generate'
             )
    parser.add_argument('--outfile', '-o'
             , required = False, default = 'results.tiff'
             , help = 'Output file (TIFF)'
             )
    parser.parse_args(namespace=args_)
    main(**vars(args_))
