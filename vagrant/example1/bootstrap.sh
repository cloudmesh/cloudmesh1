#!/usr/bin/env bash


case $(id -u) in
    0)
		# # runs as root
		sudo -u vagrant -i $0  # script calling itself as the vagrant user
		;;
	*)
		echo "Running as Vagrant User"
		# Requirements
		sudo apt-get update
		sudo apt-get -y install git
		sudo apt-get -y install python-pip
		sudo apt-get -y install python-virtualenv

		# Cloudmesh
		cd /home/vagrant/
		git clone https://github.com/cloudmesh/cloudmesh.git
		git clone https://github.com/cloudmesh/cmd3.git
		chown -R vagrant:vagrant cloudmesh
		chown -R vagrant:vagrant cmd3

		# Create a Virtual Environment 
		virtualenv ~/ENV
		source ~/ENV/bin/activate
		cd /home/vagrant/cmd3
		python setup.py install
		cd /home/vagrant/cloudmesh
		echo -e "\nsource ~/ENV/bin/activate\ncd ~/cloudmesh\n" >> ~/.bashrc

		# Setup the system
		sudo ./install system
		cd ~/cloudmesh
		./install requirements
		./install new

		# Copy private key from shared directory to .ssh
		cp /vagrant/id_rsa ~/.ssh/id_rsa
		cp /vagrant/id_rsa.pub ~/.ssh/id_rsa.pub
		ssh-keygen -y -f ~/.ssh/id_rsa > ~/.ssh/id_rsa.pub
		ssh-keygen -b 2048 -t rsa -f ~/.ssh/cloudmesh-default -q -N ""

		# Install cloudmesh and other user related stuff
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
		;;
esac