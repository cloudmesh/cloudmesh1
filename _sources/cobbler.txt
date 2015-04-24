
Cloudmesh Installation wit Cobbler Integration
======================================================================

This section is not yet complete and is only intended for an expert. Regular users will not do this.

Install Ubuntu 14.04
----------------------------------------------------------------------

When use Dell Server, please use the eth1 interface which is the top port generally. If you make a wrong choice, after install finished you can config it manually::

     command> vi /etc/network/interfaces
     edit> change eth0 to eth1
     edit> save and quit the file
     command> reboot the computer

Refresh Ubuntu update sources::

	command> sudo apt-get update

Prepare the system
----------------------------------------------------------------------

Install and configure git::

	command> sudo apt-get install git
	command> git config --global user.name "your full name"
	command> git config --global user.email "your email address"

Install openssh-server::

	command> sudo apt-get install openssh-server
	
Config openssh-server.

Create the .ssh directory::

	command> mkdir -p ~/.ssh
	command> chmod 700 ~/.ssh

Add user public key to .ssh/authorized_keys::

	command> cat your_id_rsa.pub >> ~/.ssh/authorized_keys
	command> chmod 600 ~/.ssh/authorized_keys

Disable password authentication::

	command> sudo cp /etc/ssh/sshd_config /etc/ssh/sshd_config.factory-defaults
	command> sudo vi /etc/ssh/sshd_config
	edit> change the line "#PasswordAuthentication yes" to "PasswordAuthentication no"
	edit> save and quit the file
	command> sudo restart ssh

Install Cloudmesh 	
----------------------------------------------------------------------

Get Cloudmesh::

	command> git clone https://github.com/cloudmesh/cloudmesh.git

Test git push, modify a file::

	command> vi ~/cloudmesh/cloudmesh/cobbler/demo.py
	edit> add a simple print statement on the end of the file
	edit> save and quit
	command> git add cloudmesh/cobbler/demo.py
	command> git commit -m "only for test git"
	command> git push
	command> you need to input your username and password on github.com
	
Install pip::

	command> sudo apt-get install python-setuptools
	command> sudo easy_install pip
	
Install virtualenv and configure virtualenv::

	command> sudo pip install virtualenv
	command> virtualenv --no-site-packages ~/ENV
	command> source ~/ENV/bin/activate
	command> echo "source ~/ENV/bin/activate" >> ~/.bashrc 

Install Fabric::

	command> sudo apt-get install python-dev
	command> pip install fabric
	
Install requirements.txt::

	command> sudo apt-get install libldap2-dev
	command> sudo apt-get install libsasl2-dev
	command> pip install -r requirements.txt
	
Install mongodb::

	command> sudo apt-get install mongodb-server
	
Install PIL (zip decoder for rackdiag) [optional]::

	command> sudo apt-get build-dep python-imaging
	command> apt-get install libjpeg8 libjpeg8-dev libpng3 
	command> apt-get install libfreetype6-dev
	command> sudo ln -s /usr/include/freetype2 /usr/include/freetype	
	
Install rackdiag or nwdiag [optional]::

	command> pip install nwdiag
	
Install pika [optional]::

	command> pip install pika
	
Install matplotlib [optional]::

	command> sudo apt-get build-dep python-matplotlib
	command> pip install -f http://sourceforge.net/projects/matplotlib/files/matplotlib/matplotlib-1.3.0/matplotlib-1.3.0.tar.gz matplotlib

Cobbler
----------------------------------------------------------------------
	
FIX cobbler installation on i71 [optional]

Install debmirror, because sudo cobbler check cannot pass::

	command> sudo yum install debmirror

comment out dists and arches in /etc/debmirror.conf
	
Install and configure Cloudmesh::

    command> fab build.install
    command> fab mongo.boot
    command> fab mongo.admin
    command> fab mongo.start
    command> fab mongo.inventory
    command> fab user.mongo
    command> fab mongo.stop
   	
Start Cloudmesh::

    command> fab server.agent
    command> fab server.start
	
		
