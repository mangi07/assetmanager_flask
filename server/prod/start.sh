#! /bin/bash

sudo docker run --name bu-prod -d -p 80:80 -v $(pwd)/../../:/var/www/ bu-prod-image
