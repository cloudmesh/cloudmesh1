all:
	make -j -f Makefile $(SERVER)-start

help:
	@echo "usage"
	@echo "      make SERVER=home"
	@echo "      make SERVER=server"

$(SERVER)-start: $(SERVER) view


home:
	python home.py 

server:
	python server.py 

view:
	sleep 1
	open http://localhost:5000