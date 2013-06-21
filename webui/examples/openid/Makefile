all: 
	make -j -f Makefile run

run: db server view

db:
	python startdb.py

server:
	python example.py

view:
	sleep 1
	open http://localhost:5000