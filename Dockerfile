FROM nginx
EXPOSE 80
COPY public /usr/share/nginx/html
COPY conf-staging /etc/nginx/conf.d
