rm -rf /tmp/vagrant/cloudmesh
mkdir -p /tmp/vagrant/cloudmesh
cd /tmp/vagrant/cloudmesh
git clone git@github.com:cloudmesh/cloudmesh.git
vagrant init ubuntu-14.04-server-amd64
vagrant up
vagrant ssh

