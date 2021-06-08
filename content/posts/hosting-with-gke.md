+++ 
draft = true
date = 2021-05-28T20:28:58-04:00
title = "How I Host this Site"
description = "Hosting static content with Google Kubernetes Engine"
slug = ""
authors = ["Tom"]
tags = ["GKE","Kubernetes","static-site"]
categories = []
externalLink = ""
series = ["site-automation"]
+++

In my [last post](/posts/building-with-hugo/), I explained how I am building this site with [Hugo](https://gohugo.io/), but stopped short of explaining how I am hosting it.
In this post, I'll take you through a bit of how Kubernetes works and explain how I'm using it to host the site you're looking at.

##### What is Kubernetes?

[Kubernetes](https://kubernetes.io/) is an orchestration system for automating a range of container-oriented tasks; think things like deployment, scaling, and self-healing.
While Kubernetes is well-suited for a variety of applications, its traditional application is running [twelve-factor](https://12factor.net/) web apps.
There is a lot to Kubernetes, and an exhaustive tour is beyond the scope of this post, but I'll try to provide a brief background and explain each piece as I go.

In the beginning, web apps were run on physical servers.
When an organization approached their server capacity, they were forced to buy more.
This created obvious planning and resource-utilization headaches, the most ironic being servers unable to handle a sudden influx in traffic due to a web app going viral.
Broadly the industry would settle on a more sharing-economy approach to computing power, democratizing access to scalable resources with pay-as-you-go pricing.
For SaaS, container technology, combined with the ability to automatically create additional VMs via a cloud provider, meant the tools are now there for even small organizations to automate this problem away.

And scalability is just one of many concerns that running a web app raises.

What if a container goes down? 
How do you recognize that and recover? 
If you are running your app across multiple containers, how do you balance traffic between them?

There are many ways to solve these, but organizations having extensive experience with these types of problems settle on certain approaches being better than others.
In one particular case, Google came up with a packaged set of tools written in GoLang based on their own needs. 
They open-sourced the project and provided it as a free-to-use tool that can integrates with cloud APIs.

They named that tool Kubernetes.

##### Building an Image

First I'll need an image to run, so I'll build it from my Dockerfile and push it up to [Google Container Registry](https://cloud.google.com/container-registry).
My Dockerfile is about as simple as it gets:

{{< highlight docker >}}
FROM nginx
EXPOSE 80
COPY public /usr/share/nginx/html
{{< /highlight >}}

My base image is nginx, a lightweight webserver.
The Dockerfile exposes the standard http port and copies the contents of my public folder to a folder that nginx will look to for serving static content.
In my last post the public was created when I ran ```hugo``` to generate the html and other files needed for seeing my content outside of Hugo's built-in local server.

Now I'll build the image.

{{< highlight bash >}}
tom@ubuntu:~/git/thomasflanigan$ docker build -t $TOMS_SITE_IMG .
Sending build context to Docker daemon  7.965MB
Step 1/3 : FROM nginx
latest: Pulling from library/nginx
69692152171a: Pull complete
30afc0b18f67: Pull complete
596b1d696923: Pull complete
febe5bd23e98: Pull complete
8283eee92e2f: Pull complete
351ad75a6cfa: Pull complete
Digest: sha256:6d75c99af15565a301e48297fa2d121e15d80ad526f8369c526324f0f7ccb750
Status: Downloaded newer image for nginx:latest
---> d1a364dc548d
Step 2/3 : EXPOSE 80
---> Running in 9da7a9dd02cc
Removing intermediate container 9da7a9dd02cc
---> 62f1ae442966
Step 3/3 : COPY public /usr/share/nginx/html
---> e1670ad1b9a4
Successfully built e1670ad1b9a4
Successfully tagged gcr.io/[GCP_PROJECT_ID]/thomasflanigan:latest
{{< /highlight >}}

I've set an environment variable TOMS_SITE_IMG in the format gcr.io/[GCP_PROJECT_ID]/[IMAGE_NAME]:[IMAGE_TAG].
Before pushing it out to the registry, I'll run ```docker run -p 8080:80 $TOMS_SITE_IMG``` and navigate to http://localhost:8080 to see that site is hosted in the container correctly.
This might look like a bit of magic.
By poking around interactively within the container, I can get a better picture of how this uses the default nginx configuration coming from my image's base layer.

{{< highlight bash >}}
tom@ubuntu:~/git/thomasflanigan$ docker run -it $TOMS_SITE_IMG /bin/bash
root@6113c3fcd402:/# cat /etc/nginx/nginx.conf

user  nginx;
worker_processes  1;

error_log  /var/log/nginx/error.log warn;
pid        /var/run/nginx.pid;


events {
worker_connections  1024;
}


http {
include       /etc/nginx/mime.types;
default_type  application/octet-stream;

    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';

    access_log  /var/log/nginx/access.log  main;

    sendfile        on;
    #tcp_nopush     on;

    keepalive_timeout  65;

    #gzip  on;

    include /etc/nginx/conf.d/*.conf;
}
{{</ highlight >}}

```/etc/nginx/nginx.conf``` is where nginx looks for its configuration. 
I could copy my own version of this file into the image and overwrite this one if I needed something more custom.
At the bottom of the configuration I can see that everything with a .conf in the /etc/nginx/conf.d/ directory will be included in the configuration.
Still from in the container:

{{< highlight bash >}}
root@6113c3fcd402:/# ls /etc/nginx/conf.d/
default.conf
root@6113c3fcd402:/# cat /etc/nginx/conf.d/default.conf
server {
listen       80;
server_name  localhost;

    #charset koi8-r;
    #access_log  /var/log/nginx/host.access.log  main;

    location / {
        root   /usr/share/nginx/html;
        index  index.html index.htm;
    }

    #error_page  404              /404.html;

    # redirect server error pages to the static page /50x.html
    #
    error_page   500 502 503 504  /50x.html;
    location = /50x.html {
        root   /usr/share/nginx/html;
    }

    # proxy the PHP scripts to Apache listening on 127.0.0.1:80
    #
    #location ~ \.php$ {
    #    proxy_pass   http://127.0.0.1;
    #}

    # pass the PHP scripts to FastCGI server listening on 127.0.0.1:9000
    #
    #location ~ \.php$ {
    #    root           html;
    #    fastcgi_pass   127.0.0.1:9000;
    #    fastcgi_index  index.php;
    #    fastcgi_param  SCRIPT_FILENAME  /scripts$fastcgi_script_name;
    #    include        fastcgi_params;
    #}

    # deny access to .htaccess files, if Apache's document root
    # concurs with nginx's one
    #
    #location ~ /\.ht {
    #    deny  all;
    #}
}
{{</ highlight >}}

From the location section within the server directive we can see that nginx is using ```/usr/share/nginx/html``` to look for content. 
Nginx will serve any index.html files for paths under that location, the same one my Dockerfile copies my content to.
So the "magic" is really just relying on the default nginx configuration coming from the base image.

Finally, I'll push the image up to the registry.

{{< highlight bash >}}
tom@ubuntu:~/git/thomasflanigan$ docker push $TOMS_SITE_IMG
Using default tag: latest
The push refers to repository [gcr.io/GCP_PROJECT_ID/thomasflanigan:latest]
35e0dc2a6cbb: Pushed
075508cf8f04: Layer already exists
5c865c78bc96: Layer already exists
134e19b2fac5: Layer already exists
83634f76e732: Layer already exists
766fe2c3fc08: Layer already exists
02c055ef67f5: Layer already exists
latest: digest: sha256:2a22fffa87737085ec8b9a1f13fff11f9b78d5d7a3d9e53d973d2199eae0dbdc size: 1781
{{</ highlight >}}

##### Kubernetes Controllers
