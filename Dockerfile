FROM nginx
EXPOSE 80
COPY output /usr/share/nginx/html
