#!/bin/bash



destConfPath="nginx_config/etc/nginx/sites-available/assetmanager.conf"

echo -n "Enter the domain name or IP address of the server for which you want to set up SSH: "
read address
echo "Address $address is now being added to $destConfPath..."
x=$(<assetmanager.conf)
echo "${x/'<<domain>>'/$address}" > $destConfPath
echo "Finished adding $destConfPath..."


echo "Building docker image for production server..."
sudo docker build --build-arg request_domain=$address -t bu-prod-image .

