cd cd /tmp/github/veewee
bundle exec veewee vbox define 'ubuntu-14.04-server-amd64' 'ubuntu-14.04-server-amd64'
bundle exec veewee vbox build 'ubuntu-14.04-server-amd64'
bundle exec veewee vbox export 'ubuntu-14.04-server-amd64'
vagrant box add ubuntu-14.04-server-amd64 ubuntu-14.04-server-amd64.box
