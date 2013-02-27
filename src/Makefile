deprecated:
	@echo "This Makefile is deprecated, pelase use the fab command"

.PHONY: cm 

TAG=`cat VERSION.txt`

SERVER=server
 
all:
	make -j -f Makefile $(SERVER)-start

cleantest:
	python cloud_mesh.py
	make -f Makefile cm

$(SERVER)-start: $(SERVER) view


$(SERVER): 
	python $(SERVER).py 

view:
	sleep 1
	open http://localhost:5000/table

clean:
	find . -name "#*" -exec rm {} \;  
	find . -name "*~" -exec rm {} \;  
	find . -name "*.pyc" -exec rm {} \;  
	rm -rf build dist *.egg-info 

git:
	make clean
	git add .
	git commit 
	git push

tag:
	make clean
	python bin/util/next_tag.py
	git tag $(TAG)
	echo $(TAG) > VERSION.txt
	git add .
	git commit -m "adding version $(TAG)"
	git push

change:
	CURRENT=`git describe --abbrev=0 --tags`
	echo $(CURRENT)
	#@echo "logged changes"
	#git log $(OLD)...$(NEW) --no-merges --format="* %B"
	#cp VERSION.txt /tmp


install:
	pip install Flask Frozen-Flask Flask-FlatPages