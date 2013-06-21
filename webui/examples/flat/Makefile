.PHONY: cm 

TAG=`cat VERSION.txt`

SERVER=server

all:
	make -j -f Makefile $(SERVER)-start

$(SERVER)-start: $(SERVER) view

$(SERVER):
	python $(SERVER).py 

view:
	sleep 1
	open http://localhost:5000

clean:
	find . -name "*~" -exec rm {} \;  
	find . -name "*.pyc" -exec rm {} \;  
	rm -rf build dist *.egg-info *~ #*

install:
	pip install Flask Frozen-Flask Flask-FlatPages