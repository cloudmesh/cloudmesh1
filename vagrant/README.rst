Setup
======================================================================

you must have the ubuntu 14.04 in vagrant. There is a images/veewee directory that can help you do this. 

cd images/veewee; veewee

After you got your box into vagrant you can say

mkdir vagrant
cd vagrant
git clone https://github.com/cloudmesh/cloudmesh.git

cp -r cloudmesh/vagrant/Vagrantfile .

Use
======================================================================

vagrant up
vagrant ssh
