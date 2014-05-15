echo "# #####################################################################"
echo "# preparing Ubuntu for cloudmesh" 
echo "# ######################################################################"
PACKAGES="emacs24
  git
  python-setuptools
  python-dev
  libldap2-dev
  libsasl2-dev
  libssl-dev
  python-virtualenv
"
echo "This will install (if not already installed):"
for P in $PACKAGES; do
  echo "    $P"
done
# http://stackoverflow.com/questions/226703/how-do-i-prompt-for-input-in-a-linux-shell-script
while true; do
    read -p "Do you wish to proceed? " yn
    case $yn in
        [Yy]* ) break;;
        [Nn]* ) echo "Exiting..."; exit;;
        * ) echo "Please answer yes or no.";;
    esac
done
sudo apt-get -y install $PACKAGES



