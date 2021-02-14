#!/bin/bash

destConfPath="./assetmanager.conf"

echo -n "Enter the domain name or IP address of the server for which you want to set up SSH: "
read address

echo "Address $address is now being added to $destConfPath"

x=$(<assetmanager.conf)
echo "${x/'<<domain>>'/$address}" > $destConfPath
echo "Finished adding $destConfPath"

sudo docker build --build-arg request_domain=$address -t bu-image .

