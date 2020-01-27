OUTFILE =  results.tiff

all : $(OUTFILE)

$(OUTFILE) : ./grid_generator.py
	rm -rf ./frames/*
	python3 $< -N 500 -H 29 -W 29 --num-brights 10 --num-fixed-brights 2 \
	    --gap 3 \
	    -o $(OUTFILE)

install :
	python3 -m pip install -r ./requirements.txt --user

pngs: $(OUTFILE)
	rm -rf frames
	mkdir -p frames
	# See here http://www.imagemagick.org/script/command-line-options.php?#resize
	  convert \
	  -filter box -resize 2000% \
	  $< frames/f%04d.png

gif : $(OUTFILE)
	convert $< -resize 100x100 $(OUTFILE).gif

