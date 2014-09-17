#!/usr/bin/env bash

# runs as root

# Requirements
apt-get update
apt-get -y install git
apt-get -y install python-pip
#pip install virtualenv
apt-get -y install python-virtualenv

# Cloudmesh
git clone https://github.com/cloudmesh/cloudmesh.git ~/cloudmesh/
git clone https://github.com/cloudmesh/cmd3.git ~/cmd3
virtualenv ~/ENV
source ~/ENV/bin/activate
cd ~/cmd3
python setup.py install
cd ~/cloudmesh
echo -e "\nsource ~/ENV/bin/activate\ncd ~/cloudmesh\n" >> ~/.bashrc
./install system
./install requirements
./install new

# Copy private key from shared directory to .ssh
cp /vagrant/id_rsa ~/.ssh/id_rsa
ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub
ssh-keygen -b 2048 -t rsa -f ~/.ssh/cloudmesh-default -q -N ""
./install cloudmesh
cm-iu user fetch --username=`cat /vagrant/.userid`
cm-iu user create
fab mongo.boot
fab user.mongo:cloudmesh
fab mongo.simple
# fab mongo.reset is same as fab mongo.boot, user.mongo, mongo.simple
#fab mongo.reset
fab server.start
cm cloud on india
cm flavor india --refresh
