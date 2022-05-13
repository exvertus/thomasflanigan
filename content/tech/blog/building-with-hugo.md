Title: "How I Built this Site"
Summary: "Building static content with hugo"
Date: 2021-05-17
Tags: tech, how-to, static-site-builds
Slug = building-with-hugo

I have been using more cloud tools these days and had an itch to start a blog about it.
I have a dev ops background without much front-end web experience, 
so I was happy to find out about tools like [Jekyll](https://jekyllrb.com/) and [Hugo](https://gohugo.io/); a good topic for my first post.

##### Jekyll vs Hugo

Jekyll and Hugo are both site generators. 
Hugo struck me as a better fit due to its speed when compared with Jekyll. 
With the ```hugo serve``` command, I can update files and see the html rendered on a live local server.
It is a nice feature for maintaining a tight feedback loop for staying in a flow state.

##### Create a Hugo Project

First I'll need to [install hugo](https://gohugo.io/getting-started/installing/) and create a repository. 
I've named mine hugo-demo.
Note since I have already created the repository on github, I'll need to use ```--force``` when creating the site.

{{< highlight bash >}}
tom@ubuntu:~/git$ git clone git@github.com:exvertus/hugo-demo.git
Cloning into 'hugo-demo'...
remote: Enumerating objects: 3, done.
remote: Counting objects: 100% (3/3), done.
remote: Total 3 (delta 0), reused 0 (delta 0), pack-reused 0
Receiving objects: 100% (3/3), done.
tom@ubuntu:~/git$ hugo new site hugo-demo --force
Congratulations! Your new Hugo site is created in /home/tom/git/hugo-demo.

Just a few more steps and you're ready to go:

1. Download a theme into the same-named folder.
   Choose a theme from https://themes.gohugo.io/ or
   create your own with the "hugo new theme <THEMENAME>" command.
2. Perhaps you want to add some content. You can add single files
   with "hugo new <SECTIONNAME>/<FILENAME>.<FORMAT>".
3. Start the built-in live server via "hugo server".

Visit https://gohugo.io/ for quickstart guide and full documentation.
{{< /highlight >}}

This will add some files and folders to the root of the repository.

{{< highlight bash >}}
tom@ubuntu:~/git$ cd hugo-demo/
tom@ubuntu:~/git/hugo-demo$ ls
archetypes  config.toml  content  data  layouts  README.md  static  themes
{{< /highlight >}}

Hugo will look to config.toml for the project's global config (although this may be configured in [other ways](https://gohugo.io/getting-started/configuration/)).
It should look something like this:

{{< highlight toml >}}
baseURL = "http://example.org/"
languageCode = "en-us"
title = "My New Hugo Site"
{{< /highlight >}}

Which I'll update to be less generic.

{{< highlight toml >}}
baseURL = "http://thomasflanigan.com/"
languageCode = "en-us"
title = "Tom's New Hugo Site"
{{< /highlight >}}

##### Adding a Theme

Before I can serve the site I'll need to choose a theme. 
Hugo has [hundreds of pre-built themes](https://themes.gohugo.io/), but you may also [create your own](https://gohugo.io/commands/hugo_new_theme/).
I am using the [coder theme](https://themes.gohugo.io/hugo-coder/) for my site.
I'll add it to my config.toml:

{{< highlight toml >}}
baseURL = "http://thomasflanigan.com/"
languageCode = "en-us"
title = "Tom's New Hugo Site"
theme = "hugo-coder"
{{< /highlight >}}

Hugo will look to in /themes for the one I have defined in config.toml.
This is typically added as a git submodule:

{{< highlight bash >}}
tom@ubuntu:~/git/hugo-demo$ git submodule add https://github.com/luizdepra/hugo-coder.git themes/hugo-coder
Cloning into '/home/tom/git/hugo-demo/themes/hugo-coder'...
remote: Enumerating objects: 2383, done.
remote: Counting objects: 100% (1/1), done.
remote: Total 2383 (delta 0), reused 1 (delta 0), pack-reused 2382
Receiving objects: 100% (2383/2383), 2.38 MiB | 9.68 MiB/s, done.
Resolving deltas: 100% (1228/1228), done.
{{< /highlight >}}

Now I can check out the site with ```hugo serve```.

{{< highlight bash >}}
tom@ubuntu:~/git/hugo-demo$ hugo serve -D
Start building sites …

                   | EN  
-------------------+-----
Pages            |  7  
Paginator pages  |  0  
Non-page files   |  0  
Static files     |  5  
Processed images |  0  
Aliases          |  0  
Sitemaps         |  1  
Cleaned          |  0

Built in 53 ms
Watching for changes in /home/tom/git/hugo-demo/{archetypes,content,data,layouts,static,themes}
Watching for config changes in /home/tom/git/hugo-demo/config.toml, /home/tom/git/hugo-demo/themes/hugo-coder/config.toml
Environment: "development"
Serving pages from memory
Running in Fast Render Mode. For full rebuilds on change: hugo server --disableFastRender
Web Server is available at http://localhost:1313/ (bind address 127.0.0.1)
Press Ctrl+C to stop
{{< /highlight >}}

But this doesn't give me much of a site quite yet:

![Blank Site](/img/posts/building-with-hugo/blank-site.png)

So I'll add params to my config.toml.

# config.toml
{{< highlight toml >}}
baseURL = "http://thomasflanigan.com/"
languageCode = "en-us"
title = "Tom's New Hugo Site"
theme = "hugo-coder"
pygmentsStyle = "bw"

[params]
author = "Tom Flanigan"
description = "Tom Flanigan's personal website"
keywords = "blog,developer,personal,resume"
info = "Developer and Dev Ops Specialist"
avatarurl = "https://raw.githubusercontent.com/luizdepra/hugo-coder/master/exampleSite/static/images/avatar.jpg"

[[params.social]]
name = "Github"
icon = "fa fa-github"
weight = 1
url = "https://github.com/exvertus/"
[[params.social]]
name = "LinkedIn"
icon = "fa fa-linkedin"
weight = 2
url = "https://www.linkedin.com/in/thomas-flanigan/"

[[languages.en.menu.main]]
name = "About"
weight = 1
url = "about/"

[[languages.en.menu.main]]
name = "Blog"
weight = 2
url = "posts/"
{{< /highlight >}}

That's looking a bit better now:

![Site](/img/posts/building-with-hugo/site.png)

You can see a full list of parameters in the [theme's stackbit.yaml](https://github.com/luizdepra/hugo-coder/blob/master/stackbit.yaml) file with additional information in the [example config](https://github.com/luizdepra/hugo-coder/blob/master/exampleSite/config.toml).

##### Adding Content

My site will need more than a single page, so I'll need to add content so the 'About' and 'Blog' menu links don't 404.
Adding an about.md file to the root of the content folder will cause hugo to serve an /about/index.html page:

{{< highlight bash >}}
tom@ubuntu:~/git/hugo-demo$ hugo new about.md
/home/tom/git/hugo-demo/content/about.md created
{{< /highlight >}}

Hugo will automatically add some "front matter" to the top of the file that serves as metadata for the page.
I'll add some basic content for the page as well:

{{< highlight markdown >}}
---
title: "About"
date: 2021-05-20T18:00:47-05:00
draft: true
---

Hi I'm Tom. I like music, art, and technology.
{{< /highlight >}}

I'll create a first blog post too. Note I'm creating this in a subfolder named posts:

{{< highlight bash >}}
tom@tom-UX303UA:~/git/hugo-demo$ hugo new posts/first-post.md
/home/tom/git/hugo-demo/content/posts/first-post.md created
{{< /highlight >}}

{{< highlight markdown >}}
+++
draft = true
date = 2021-05-20T19:29:38-05:00
title = "My First Post"
description = "Demo Blog Post"
slug = ""
authors = []
tags = []
categories = []
externalLink = ""
series = []
+++

Hey! Check out my first post

{{</* highlight python */>}}
# An example code snippet
class Something(object):
    pass
{{</* /highlight */>}}

{{< /highlight >}}

Navigating to localhost:1313/about/ brings me directly to the about page, but going to /posts/ takes me to a list page showing each file in the content/posts folder:

![About](/img/posts/building-with-hugo/about.png)

![Posts](/img/posts/building-with-hugo/blog-list-page.png)

Taking a look at the look at my blog post, I'm not really happy with how the code snippet coloring looks against the white background:

![BwPost](/img/posts/building-with-hugo/first-post-bw.png)

I can change the 'bw' pygments coloring by editing the 'pygmentsStyle' parameter in my config.toml file. 
I'm able to preview some other choices from [this page](https://help.farbox.com/pygments.html).
I'll change pygmentsStyle to use 'monokai' instead:

{{< highlight toml >}}
# config.toml
pygmentsStyle = "monokai"
{{< /highlight >}}

![MonokaiPost](/img/posts/building-with-hugo/first-post-monokai.png)

##### Wrapping Up

I'm happy with the result and ready to generate the static content for my site.
First I'll set each content file's front matter so that they are no longer drafts.

{{< highlight toml >}}
draft: false
{{< /highlight >}}

Then I can run the ```hugo``` command from the root of the project to generate the content.
Hugo will drop the output into a folder named 'public' by default.

{{< highlight bash >}}
tom@ubuntu:~/git/hugo-demo$ hugo
Start building sites …

                   | EN  
-------------------+-----
Pages            |  8  
Paginator pages  |  0  
Non-page files   |  0  
Static files     |  5  
Processed images |  0  
Aliases          |  0  
Sitemaps         |  1  
Cleaned          |  0

Total in 79 ms
tom@ubuntu:~/git/hugo-demo$ ls public
404.html  categories  fonts       index.xml  sitemap.xml
about     css         index.html  js         tags
{{< /highlight >}}

Since the public folder contains the hugo build artifacts, I don't want anything in that folder to pollute the repository.
I'll add it, and the resources folder (hugo uses that directory as a cache), to my .gitignore

{{< highlight bash >}}
# .gitignore
public
resources
{{< /highlight >}}

##### Conclusion

That's it! Note I've used a demo repository for the purposes of this post.
If you'd like to see the live code for this site (including the code for [the page you're reading now](https://raw.githubusercontent.com/exvertus/thomasflanigan/main/content/posts/building-with-hugo.md)), you can view my [github project](https://github.com/exvertus/thomasflanigan).