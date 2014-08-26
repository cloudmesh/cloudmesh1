#!/usr/bin/env bash

apt-get -y install git
apt-get -y install python-pip
pip install virtualenv
git clone https://github.com/cloudmesh/cloudmesh.git ~/cloudmesh/
git clone https://github.com/cloudmesh/cmd3.git ~/cmd3
virtualenv ~/ENV
source ~/ENV/bin/activate
cd ~/cmd3
python setup.py install
cd ~/cloudmesh
./install system
./install requirements
./install new
cp /vagrant/id_rsa ~/.ssh/id_rsa
./install rc fetch --username=`cat /vagrant/.userid`
./install rc fill
./install cloudmesh
fab mongo.start
sleep 5
fab mongo.boot
#fab mongo.boot
sleep 5
fab user.mongo
fab mongo.simple
fab server.start
