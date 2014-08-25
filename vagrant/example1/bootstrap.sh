#!/usr/bin/env bash

apt-get -y install git
git clone https://github.com/cloudmesh/cloudmesh.git
apt-get -y install python-pip
pip install virtualenv
su -- vagrant
virtualenv ~/ENV
source ~/ENV/bin/activate
cd cloudmesh
sudo ./install system
./install requirements
./install new
#./install rc fetch
#./install rc fill
./install cloudmesh
fab mongo.start
fab mongo.boot
fab user.mongo
fab mongo.simple
fab server.start
