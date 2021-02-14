#!/bin/bash



destConfPath="nginx_config/etc/nginx/sites-available/assetmanager.conf"

echo -n "Enter the domain name or IP address of the server for which you want to set up SSH: "
read address
echo "Address $address is now being added to $destConfPath..."
x=$(<assetmanager.conf)
echo "${x/'<<domain>>'/$address}" > $destConfPath
echo "Finished adding $destConfPath..."


echo -n "Enter (1) development mode or (2) production mode: "
read mode
if [ "$mode"="1" ] ; then mode=development ; elif [ "$mode"="2" ] ; then mode=production ; fi

echo "Building docker image for $mode mode..."
sudo docker build --build-arg request_domain=$address --build-arg MODE=$mode -t bu-image .

