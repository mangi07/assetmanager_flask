run ./dockerbuild.sh
then...

run with:
sudo docker run --name bu -d -p 80:80 -v $(pwd)/../:/var/www/assetmanager/html/ bu-image

enter terminal with:
sudo docker exec -it bu bash

