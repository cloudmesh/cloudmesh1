


FG=psjoshi 


ssh $USER@india.futuregrid.org uname
ssh $USER@sierra.futuregrid.org uname
#ssh $USER@alamo.futuregrid.org uname
ssh $USER@hotel.futuregrid.org uname

mkdir .futuregird

scp -r $FG@india.futuregrid.org:.futuregrid india

scp -r $FG@sierra.futuregrid.org:.futuregrid sierra

#scp -r $FG@hotel.futuregrid.org:.futuregrid hotel





brew update
brew install mongodb

or

port install mongodb