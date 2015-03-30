#!/bin/bash

write_userid () {
	userid=$1
	echo $userid > .userid
}

select_option() {
	option=$1
	case $option in
		"Ubuntu-Server-14.04-64bit") 
			echo $option "selected"
			ln -sf .Vagrantfile_ubuntu_trusty64 Vagrantfile
			;;

		"Ubuntu-Server-14.04-32bit") 
			echo $option "selected"
			ln -sf .Vagrantfile_ubuntu_trusty32 Vagrantfile
			;;
		quit)
	esac
}

images=("Ubuntu-Server-14.04-64bit" "Ubuntu-Server-14.04-32bit")
debug=0

# copy private key to synced folders
#if [ -f ~/.ssh/id_rsa ]; then
#	cp ~/.ssh/id_rsa `pwd`
#else
#	echo "=================================="
#	echo "SSH Key file (id_rsa) is missing."
#	echo "You can generate by ssh-keygen."
#	echo "=================================="
#	exit
#fi

if [ -f ~/.ssh/id_rsa.pub ]; then
	cp ~/.ssh/id_rsa.pub `pwd`
else
	echo "=================================="
	echo "SSH Key file (id_rsa) is missing"
	echo "You can generate one with ssh-keygen."
	echo "=================================="
	exit
fi

if [ $# -eq 2 ]
then
	userid=$1
	option=$2
fi

if [ -z "$userid" ]
then
	echo "=================================="
	echo "Futuregrid portal id? (def:$USER)"
	echo "=================================="
	echo -n "Login id: "; read userid
fi
write_userid "$userid"

if [ -z "$option" ]
then
	echo
	echo "=================================="
	echo "Select base image to launch"
	echo "=================================="
	PS3="Please choose an option: "
	select option in ${images[@]}
	do
		select_option "$option"
		break;
	done
else
	select_option "$option"
fi

# Verify
if [ 0 -ne "$debug" ]
then
	cat .userid
	ls -al Vagrantfile
fi

echo
echo "=================================="
echo "Vagrant is up"
echo "=================================="
vagrant up
