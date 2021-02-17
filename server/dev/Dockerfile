FROM ubuntu:20.04

RUN apt update -y && apt upgrade -y
RUN apt install neovim -y ; \
	apt install nodejs -y ; \
	apt install npm -y ; \
	apt install python3-pip -y ; \
	apt install python3-venv -y ; \
	apt install git -y ; \
	apt install tree -y ;

# ###############################################
# install and configure nginx
RUN apt install nginx -y
RUN mkdir -p /var/www/
RUN chmod -R 755 /var/www/

COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./assetmanager.conf /etc/nginx/sites-available/assetmanager.conf
RUN ln -s /etc/nginx/sites-available/assetmanager.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default
COPY ./dhparam.pem /etc/nginx/dhparam.pem

# ###############################################
# get ssl certificate
ARG request_domain
#ENV request_domain=$request_domain

RUN apt install openssl && \
	openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out /etc/ssl/certs/nginx-selfsigned.crt \
            -keyout /etc/ssl/private/nginx-selfsigned.key \
            -subj "/C=GU/ST=GU/L=Hagatna/O=Self/OU=Dev/CN=$request_domain" ;
	#openssl dhparam -out /etc/nginx/dhparam.pem 4096 \

# ###############################################
# start server
EXPOSE 80
#CMD service nginx start
CMD ["nginx", "-g", "daemon off;"]
