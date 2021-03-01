run ./build.sh
then...

run with:
sudo docker run --name bu-prod -d -p 80:80 -v $(pwd)/../:/var/www/assetmanager/html/ bu-prod-image

enter terminal with:
sudo docker exec -it bu-prod bash

