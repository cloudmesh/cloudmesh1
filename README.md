Documentation will be at 

http://futuregrid.github.com/cm

However currently look at the source

module load git
module load python

virtualenv TEST

source TEST/bin/activate

mkdir test

git clone git@github.com:futuregrid/cm.git

cd cm

make

chmod a+x ~/TEST/bin/cm 

cd src

source ~/.futuregrid/openstack/novarc 

cm r
