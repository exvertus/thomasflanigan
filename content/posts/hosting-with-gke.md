+++ 
draft = true
date = 2021-05-28T20:28:58-04:00
title = "How I Host this Site"
description = "Hosting static content with Google Kubernetes Engine"
slug = ""
authors = ["Tom"]
tags = ["GKE","static-site"]
categories = []
externalLink = ""
series = ["site-automation"]
+++

In my [last post](/posts/building-with-hugo/), I explained how I am building this site with [Hugo](https://gohugo.io/), but stopped short of explaining how I am hosting the site.
In this post I'll take you through a bit of how Kubernetes works and explain how I'm using it to run the site.

##### What is Kubernetes?

[Kubernetes](https://kubernetes.io/) is an orchestration system for automating a range of container-oriented tasks for things like deployment, scaling, and self-healing.
While Kubernetes is well-suited for a variety of applications, its traditional application is running [twelve-factor](https://12factor.net/) web apps.
There is a lot to Kubernetes, and an exhaustive tour is beyond the scope of a blog post, but to good way to get the gist of it is to understand some history and the problems Kubernetes helps solve.

In the beginning, web apps were run on physical servers.
As organizations approached their server capacity, it was time to buy more servers.
This created obvious planning and resource-utilization headaches, perhaps the worst being servers not handling a sudden influx in traffic due to the web app going viral, missing a massive opportunity.
Container technology, combined with the ability to automatically create additional VMs via a cloud provider, meant the tools were there for even small organizations to automate this problem.

And scalability is just one of many concerns that running a web app raises.
TODO: Come up with saying better than 'skin a cat'
What if a container goes down? 
How can you recognize that and recover? 
If you are running your app across multiple containers, how do you balance traffic between them? 
There are many ways to skin a cat, but over time some ways to automate these things became more common and won out over others.

