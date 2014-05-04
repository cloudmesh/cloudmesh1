Vagrant
==================

Issues with vagrant

* default passwords
* insecure keys

Do not put your vagrant vm publicly on the net.

Veewee
=============

Creating a base box for ubuntu 14.04::

  mkdir github
  cd github
  git clone git@github.com:jedi4ever/veewee.git
  cd veewee
  bundle install
  bundle exec veewee vbox define 'ubuntu-14.04-server-amd64' 'ubuntu-14.04-server-amd64'
  bundle exec veewee vbox build 'ubuntu-14.04-server-amd64'
  
Now you could logging into the image::

  ssh -o UserKnownHostsFile=/dev/null -o StrictHostKeyChecking=no -p 7222 -l vagrant 127.0.0.1

Exporting::

   bundle exec veewee vbox export 'ubuntu-14.04-server-amd64'


.. note: 

   the following 'adding' does not work

Adding::

  vagrant box add ubuntu-14.04-server-amd64 ubuntu-14.04-server-amd64.box

To use it::

   mkdir mytest
   cd mytest
   vagrant init 'ubuntu-14.04-server-amd64'
   vagrant up
   vagrant ssh

If you like to find other boxes you can find some with the command::

  bundle exec veewee vbox templates | grep -i ubuntu
