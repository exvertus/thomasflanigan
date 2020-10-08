FROM nginx
EXPOSE 80
COPY content/_site /usr/share/nginx/html
