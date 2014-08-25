#!/usr/bin/env bash

git clone https://github.com/cloudmesh/cloudmesh.git
virtualenv ~/ENV
source ~/ENV/bin/activate
cd cloudmesh
./install system
./install requirements
./install new
#./install rc fetch
#./install rc fill
./install cloudmesh
fab mongo.start
fab mongo.boot
fab user.mongo
fab mongo.simple
fab server.start
