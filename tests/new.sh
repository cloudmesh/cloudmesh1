#! /bin/sh

cd ~
deactivate
rm -rf TEST
virtualenv TEST -p /usr/local/bin/python
source ~/TEST/bin/activate
which python
# pip install cmd3
# pip install cloudmesh_base

# echo "######################################################################"
# echo "Running tests"
# echo "######################################################################"

# rm -rf ~/NOSETESTS
# mkdir ~/NOSETESTS


PACKAGE=cloudmesh

# cd ~/NOSETESTS

git clone git@github.com:cloudmesh/$PACKAGE.git
cd $PACKAGE
python setup.py install

# nosetests --nocapture -v database.py
#nosetests --nocapture -v tests/submit.py
