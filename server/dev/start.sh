#! /bin/bash

sudo docker run --name bu -d -p 80:80 -v $(pwd)/../../:/var/www/ bu-image
