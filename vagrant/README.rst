Setup
======================================================================

you must have the ubuntu 14.04 in vagrant. There is a images/veewee directory that can help you do this. 

cd images/veewee; veewee

After you got your box into vagrant you can say

mkdir ~/vagrant
cp -r ../cloudmesh/vagrant ~/vagrant
cp vagrant/Vagrantfile ~/vagrant 
cd ~/vagrant

Use
======================================================================

vagrant up
vagrant ssh

Bugs
we need to have a bashrc file with the virtual env activated 

do by hand after login 

. ~/ENV/bin/activate
