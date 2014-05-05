You should have a templates subdirectory within your veewee working directory:

$ veewee vbox help templates
# Should list working directory within the help command.

# within the templates there are sub-directories for each
$ veewee vbox templates | grep ubuntu

# You can copy one of these to create an ubuntu-14.04. For example:
$ cp -r ubuntu-12.04.4-server-amd64 ubuntu-14.04-server-amd64

# Open the definition.rb file. This is where the download URL, md5, etc. are found. I'm attaching my ubuntu-14.04 template directory as a tarball.
# NOTE: You can download the iso and place it in the iso directory and it will not redownload
# NOTE: You can also modify what post scripts are executed. For example, if you want to install (or not) Puppet, Salt Stack, etc. on the box.

Then once the Veewee vbox is created you can export it to a Vagrant box.
