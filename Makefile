all : ./grid_generator.py
	rm -rf ./frames/*
	python3 $< -N 100 -H 29 -W 29 --num-brights 10 --num-fixed-brights 2

install :
	python3 -m pip install -r ./requirements.txt --user
