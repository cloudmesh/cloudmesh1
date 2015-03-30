#! /bin/sh

cd ~
deactivate
rm -rf TEST
PYTHON_BINARY=$(which python)
virtualenv TEST -p "$PYTHON_BINARY"
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

pip install $PACKAGE

cm help

# nosetests --nocapture -v database.py
#nosetests --nocapture -v tests/submit.py
