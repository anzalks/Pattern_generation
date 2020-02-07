#!/usr/bin/env bash
set -u
set -e
set -x
rm -rf frames
mkdir -p frames
# See here http://www.imagemagick.org/script/command-line-options.php?#resize
convert  -filter box -resize 100%  $1 frames/f%04d.png

