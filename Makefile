OUTFILE =  results.tiff

all : ./grid_generator.py
	rm -rf ./frames/*
	python3 $< -N 100 -H 10 -W 10 --num-brights 10 --num-fixed-brights 1 \
	    --gap 1 \
	    -o $(OUTFILE)

install :
	python3 -m pip install -r ./requirements.txt --user

pngs: $(OUTFILE)
	rm -rf frames
	mkdir -p frames
	convert $< frames/f%04d.png
