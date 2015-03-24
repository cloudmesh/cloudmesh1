echo "# #####################################################################"
echo "# preparing Ubuntu for cloudmesh" 
echo "# ######################################################################"
PACKAGES="
  curl
  emacs24
  git
  libffi-dev
  libldap2-dev
  libsasl2-dev
  libssl-dev
  libpng-dev
  libyaml-dev
  mercurial
  mongodb-server
  python-dev
  python-setuptools
  python-virtualenv
  rabbitmq-server
  graphviz
  libffi-dev
"
echo "This will install (if not already installed):"
for P in $PACKAGES; do
  echo "    $P"
done
sudo apt-get update
sudo apt-get -y install $PACKAGES



