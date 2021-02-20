from flask import request


def get_pagination_limit():
    return 5

def get_precision_factor():
    return 10000000000.0

def get_host_url():
    # uncomment this if outside docker
    #return request.host_url

    # in case nginx has the following block:
	#location /api {
	#	proxy_pass http://localhost:5000/;
	#}
    return "http://localhost/api/"
