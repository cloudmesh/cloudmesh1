#!/bin/bash
echo -e "\n# Added by Cloudmesh\n# Fixing india routing problem\n172.29.200.136\tindia\tindia.futuregrid.org" | sudo tee -a /etc/hosts
echo -e "172.29.200.57\t\ti57r.idp.iu.futuregrid.org" | sudo tee -a /etc/hosts

