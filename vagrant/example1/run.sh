#!/bin/bash

# copy private key to synced folders
cp ~/.ssh/id_rsa `pwd`

echo "=================================="
echo "Futuregrid portal id? (def:$USER)"
read userid
echo "=================================="
echo $userid >> .userid

echo
echo "=================================="
echo "Select base image to launch"
echo "=================================="
PS3="Please choose an option: "
select option in "Ubuntu Server 14.04 64bit" "Ubuntu Server 14.04 32bit"
do
	case $option in
		"Ubuntu Server 14.04 64bit") 
			echo $option "selected"
			ln -sf Vagrantfile64 Vagrantfile
			break;;

		"Ubuntu Server 14.04 32bit") 
			echo $option "selected"
			ln -sf Vagrantfile32 Vagrantfile
			break;;
		quit)
			break;;
	esac
done

vagrant up
