FROM ubuntu:18.04

# TODO: test production build

ARG MODE

RUN apt-get update -y && apt-get upgrade -y

#RUN apt-get install software-properties-common -y # may need for production build?
#RUN apt-get update # may need for production build?

# ###############################################
# optional editing tools
RUN if [ "$MODE" = "development" ] ; then \
	apt install neovim -y ; \
	fi


# ###############################################
# install ssl for nginx
RUN if [ "$MODE" = "production" ] ; then \
	add-apt-repository ppa:certbot/certbot -y && apt-get update -y && \
	apt install python-certbot-nginx -y ; \
	fi

# ###############################################
# install and configure nginx
# RUN apt install systemd # may not work in docker container because of how docker runs
RUN apt install nginx -y
RUN mkdir -p /var/www/assetmanager/html
RUN chmod -R 755 /var/www/assetmanager
#COPY ./index.html /var/www/assetmanager/html/index.html
COPY ./nginx_config/etc/nginx/nginx.conf /etc/nginx/nginx.conf
COPY ./nginx_config/etc/nginx/sites-available/assetmanager.conf /etc/nginx/sites-available/assetmanager.conf
RUN ln -s /etc/nginx/sites-available/assetmanager.conf /etc/nginx/sites-enabled/
RUN rm /etc/nginx/sites-enabled/default
# TODO: Will the following line be good for production mode as well?
COPY ./nginx_config/etc/nginx/dhparam.pem /etc/nginx/dhparam.pem

# ###############################################
# get ssl certificate
ARG request_domain
#ENV request_domain=$request_domain

# TODO: use aws elastic IP and try to get free domain
RUN if [ "$MODE" = "production" ] ; then \
	certbot --register-unsafely-without-email --nginx -d $request_domain ; \
    elif [ "$MODE" = "development" ] ; then \
	apt-get install openssl && \
	openssl req -newkey rsa:4096 \
            -x509 \
            -sha256 \
            -days 3650 \
            -nodes \
            -out /etc/ssl/certs/nginx-selfsigned.crt \
            -keyout /etc/ssl/private/nginx-selfsigned.key \
            -subj "/C=GU/ST=GU/L=Hagatna/O=Self/OU=Dev/CN=$request_domain"
	#openssl dhparam -out /etc/nginx/dhparam.pem 4096
    fi


# ###############################################
# start server
EXPOSE 80
#CMD service nginx start
CMD ["nginx", "-g", "daemon off;"]
