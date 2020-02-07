PY := $(shell which python3)
OUTFILE =  results.tiff

all : $(OUTFILE)
	./tiff_to_pngs.sh $<

$(OUTFILE) : ./grid_generator.py
	rm -rf ./frames/*
	$(PY) $< -N 500 -H 29 -W 29 --num-brights 10 --num-fixed-brights 2 \
	  --gap 3 \
	  -o $(OUTFILE)

install :
	$(PY) -m pip install -r ./requirements.txt --user

gif : $(OUTFILE)
	convert $< -resize 100x100 $(OUTFILE).gif

single : single_pixel.tiff
	./tiff_to_pngs.sh $<

gif_single : single_pixel.tiff
	convert $< -filter box -resize 2000% $ ./single_gif.gif

./single_pixel.tiff: ./single_pixel.py
	$(PY) $<

