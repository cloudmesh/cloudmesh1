#!/bin/bash

# copy private key to synced folders
cp ~/.ssh/id_rsa `pwd`

echo "=================================="
echo "Futuregrid portal id? (def:$USER)"
read userid
echo "=================================="
echo $userid >> .userid
