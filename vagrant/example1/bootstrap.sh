#!/usr/bin/env bash

apt-get -y install git
apt-get -y install python-pip
pip install virtualenv
su --login vagrant
cd /home/vagrant
git clone https://github.com/cloudmesh/cloudmesh.git
git clone https://github.com/cloudmesh/cmd3.git
virtualenv /home/vagrant/ENV
source /home/vagrant/ENV/bin/activate
cd /home/vagrant/cmd3
python setup.py install
cd /home/vagrant/cloudmesh
sudo ./install system
./install requirements
./install new
cp /vagrant/id_rsa /home/vagrant/.ssh/id_rsa
/install rc fetch --username=`cat /vagrant/.userid`
/install rc fill
./install cloudmesh
fab mongo.start
fab mongo.boot
fab mongo.boot
fab user.mongo
fab mongo.simple
fab server.start
