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

There are many ways to solve these problems, but organizations having extensive experience with these types of problems settle on certain approaches being better than others.
In one particular case, Google came up with a packaged set of tools written in GoLang based on their own needs. 
They open-sourced the project and provided it as a free-to-use tool that can integrates with cloud APIs.

They named that tool Kubernetes.

##### Building an Image
