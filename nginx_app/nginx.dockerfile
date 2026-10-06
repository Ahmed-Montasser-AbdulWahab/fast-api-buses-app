FROM nginx:latest

WORKDIR /

COPY ./confs/. /etc/nginx/conf.d/

COPY ./static_files/. /usr/share/nginx/html/

COPY ./certs/. /etc/ssl/certs/

COPY ./private/. /etc/ssl/private/