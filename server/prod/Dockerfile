FROM ubuntu:20.04

# TODO: test production build


RUN apt-get update -y && apt-get upgrade -y

#RUN apt-get install software-properties-common -y # may need for production build?

# ###############################################
# install ssl for nginx
add-apt-repository ppa:certbot/certbot -y && apt-get update -y && \
apt install python-certbot-nginx -y ; \


# ###############################################
# install and configure nginx
RUN apt install nginx -y
RUN mkdir -p /var/www/assetmanager/html
RUN chmod -R 755 /var/www/assetmanager
COPY ./nginx.conf /etc/nginx/nginx.conf
COPY ./assetmanager.conf /etc/nginx/sites-available/assetmanager.conf
RUN ln -s /etc/nginx/sites-available/assetmanager.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default

# ###############################################
# get ssl certificate
ARG request_domain
#ENV request_domain=$request_domain

# TODO: Will the following line be good for production mode as well?
COPY ./dhparam.pem /etc/nginx/dhparam.pem

# TODO: use aws elastic IP and try to get free domain
RUN certbot --register-unsafely-without-email --nginx -d $request_domain ; \
	apt-get install openssl && \
	openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out /etc/ssl/certs/nginx-selfsigned.crt \
            -keyout /etc/ssl/private/nginx-selfsigned.key \
            -subj "/C=GU/ST=GU/L=Hagatna/O=Self/OU=Dev/CN=$request_domain" ; \
	#openssl dhparam -out /etc/nginx/dhparam.pem 4096 \
    fi


# ###############################################
# start server
EXPOSE 80
#CMD service nginx start
CMD ["nginx", "-g", "daemon off;"]
