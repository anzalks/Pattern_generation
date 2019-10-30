# Pattern Generation

## Dependencies

To install dependencies, use the following commands in Debian's terminal (or
equivalent).

1. sudo apt install imagemagick
2. pip3 install -r requirements.txt --user

## Pipeline

To run the pipeline, a `Makefile` is provided. Running is as easy as

```bash
$ make 
```
To change the parameters, open the `Makefile` in editor such as gEdit. Once it
is compete, a TIFF file (default `results.tiff`) will be generated in the
current working directory.

To generate PNG files from it, run `make pngs` in terminal.

## Parameters

To see the options available, run the following command in terminal.

```bash
$ python3 ./grid_generator.py -h
```

If will show the available options. For example, I get the following for
commit hash `5fb3c0f`.


```
usage: grid_generator.py [-h] [--width WIDTH] [--height HEIGHT]
                         [--num-fixed-brights NUM_FIXED_BRIGHTS]
                         [--magnification MAGNIFICATION]
                         [--num-brights NUM_BRIGHTS] [--gap GAP]
                         [--num-patterns NUM_PATTERNS] [--outfile OUTFILE]

Pattern Generator for Polygon.

optional arguments:
  -h, --help            show this help message and exit
  --width WIDTH, -W WIDTH
                        WIDTH of pattern
  --height HEIGHT, -H HEIGHT
                        WIDTH of the pattern
  --num-fixed-brights NUM_FIXED_BRIGHTS, -nFB NUM_FIXED_BRIGHTS
                        How many bright pixels must have fixed position.
  --magnification MAGNIFICATION, -m MAGNIFICATION
                        Magnification of objective lens.
  --num-brights NUM_BRIGHTS, -nB NUM_BRIGHTS
                        Number of bright pixels)
  --gap GAP, -g GAP     Gap between nearest bright neighbours. <=0 removes
                        restriction.
  --num-patterns NUM_PATTERNS, -N NUM_PATTERNS
                        Number of patterns to generate
  --outfile OUTFILE, -o OUTFILE
                        Output file (TIFF)

```
