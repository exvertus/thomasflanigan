Title: Zapier automation for LinkedIn posts
Summary: Automation 'for the little guy' will have a big impact
Date: 2022-06-26
Tags: tech, how-to, linkedin, automation, zapier
Slug: linkedin-zapier

I recently configured a bit of personal automation for myself,
and if you arrived here via my share on [LinkedIn](https://www.linkedin.com/in/thomas-flanigan/),
you've already seen it in action.
I not only wanted to share how easy it was to configure with [Zapier](https://zapier.com/),
but also why I am excited access to software automation is becoming democratized.

### what does automation get you?

As someone with a more than a few absent-minded-professor tendencies,
I knew that posting to my LinkedIn manually to announce each new post would quickly fall apart.
While things like avoiding manual errors and not having to remember each time are welcome benefits, 
I always like to emphasize my biggest reason for automating:

*The less something costs to create, the more it will be produced.*

While few may disagree with the statement in theory,
the temptation to forget in practice is very real.
I admit I 'kick the can' too often myself 
(the current lose ends in this site's repo provides a case-in-point), 
but when each productive iteration requires an arduous process that is left unchecked, 
a feeling of dread is coupled to the creation process.
It can become so internalized that it is shrugged off as a "given" cost to producing whatever could come next.

Without process improvements this can quickly give rise to a lethargic creative depression: 
new ideas increasingly fall under the shadow of 'too much of a bother'. 
Ideas carrying the potency to be big breakthroughs are ironically rejected for their potential to open a Pandora's box.
I have seen first hand how much this can hollow-out a software development team's productivity, 
but much has already been written about the impact technical debt creates in a corporate environment, 
and the stand-stills and hidden inefficiencies it can usher in if not take seriously.
I do not dismiss that debate as much as want stay focused on something much closer to my heart of late---enabling automation for the *individual*.

A proliferation of automation accessibility can solve some big problems we might not even be fully aware we have, 
but I will try to connect the dots on that broader and more speculative assertion below. 
That will be easier to do if I first show you how easy automation has helped me personally in more recent and concrete terms: 
automatically sharing to my LinkedIn each time I publish a new post on my site, this article being the first.

### How automation usually goes

So I started the process as many others with experience in the software automation world would:

1. Review the [API documentation](https://docs.microsoft.com/en-us/linkedin/) to ensure the data I require for my automation is available via public endpoint(s) in the first place.
2. Search for an existing API-client that wraps things like authentication and endpoint calls, ideally in one of my preferred programming languages.
3. Import and use the existing API-client if it is available OR write a minimal implementation of one myself.

Step 1 was easy enough. 
LinkedIn does indeed provide an [API path](https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin#creating-a-share-on-linkedin) enabling automatic sharing, including my need to [share a url](https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin#create-an-article-or-url-share).

Step 2 is where things got messy.
First I found a [python-linkedin lib](https://github.com/ozgur/python-linkedin) that looked promising, until I noticed the last update was in 2015, a year before Microsoft acquired LinkedIn. No thanks.

Next I found the more current [linkedin-api](https://github.com/tomquirk/linkedin-api). It initially seemed promising until I looked closer for how to share and could not find one. This library leans on an alternative service for its endpoints called Voyager and it looks like the share endpoint [has not been exposed](https://github.com/tomquirk/linkedin-api/issues/106) in the python lib yet. I initially tried to add the feature myself, but after going well down the path of forking the repo, configuring a dev build, setting up an account for the .env file for the tests (which make requests to the live server while also using a timer-delay to prevent throttling, resulting in minutes-long test runs) to pass, I started to question this approach. 
After looking at the code, I started to question all the time I was spending to add a fairly simple feature to a python project screaming for a refactor. 
So I went to sleep that night thinking I would be writing a minimal python client-wrapper in a utils directory of my site's repository to call from a new post-step in my Jenkinsfile after a successfull build-deploy from the 'main' branch of my site's repo...

So I think it is safe to say my experience demonstrates that even when you know what you are doing, building and configuring automation gets complicated quickly. That fact is a key to understanding a problem I have been increasingly concerned with, but that a platform I just discovered named Zapier is already fixing. 

### Discovering Zapier

It felt fitting that I should taste some of the discouragement that keeps automation prohibitive for most. 
Perhaps the frustration was the necessary motivation for getting myself out of the professional custom-software-automator box enough to find Zapier,
which I think is easy enough for someone with no programming background to use themselves.

Zapier allows you to create what they call "Zaps" that you configure for each unit of automation.
They also let me [share my Zap](https://zapier.com/shared/2a8c0753b0c2ef3026bf9487b4fb21c92db7e351) for others to refer to and copy themselves.

[My Zap](https://zapier.com/shared/2a8c0753b0c2ef3026bf9487b4fb21c92db7e351) is about as simple as you can make one. 
The trigger for activating my Zap is something that will routinely poll my site's [RSS feed](https://en.wikipedia.org/wiki/RSS).
If it finds that new content has been created recently, it will run the second LinkedIn step, which posts a share with a link back to the new post.

Punching this all in via a GUI-based configuration means you don't need to know how to read or write code to set one up yourself.
Additionally, Zapier made it pretty easy to test my LinkedIn step while in draft status by pulling the latest record from my RSS feed as test data. 
This saves me from the awkwardness of having to finalize my configuration and generate new content just to confirm the non-trigger portion is working.

While Zapier does have [paid tiers](https://zapier.com/app/billing/plans) as needs scale, most indivduals will be fine starting under the free tier and its easy use means Zapier's automation-as-a-service has value to individuals and small operations typically unable to afford contracting a coder for traditional custom automation.

### Automation Democratization? It's *about time*...

...and not just about saving people more of it. It's about time automation become widely available because of what we've *all* been missing out on.

I'll repeat the axiom I opened with here: *the less something costs to create, the more it will be produced*.

If you share my interest in economics, you may have already guessed at the inspiration for this axiom: 
"if you want more of something, subsidize it" and the inverse, "if you want less of something, tax it".
You may recall a similar price-control phenomenon,
where effective price-floors tend towards surpluses, and shortages tend to follow price-caps. 
Here the inversion is no less true: the *more* something costs to create, the *less* it will be produced.

Simply *running* most simple automations is usually not costly, 
the true cost comes in the complexity in coding, configuring and maintaining the code and infrastructure to keep it on. 
Yet corporations with software needs dedicate full-time well-paid positions so they can automate, because they have correctly idenfied its worth. 

But how well do those outside the software and IT world understand the value of automation?

When I moved to Austin I began meeting other indpendent artists and talked to a few owners of small businesses in the creative industry around town. 
Contrasting their utilization of automation against my time building it for years in the corporate tech industry, 
it felt like larger tech corporations had sailed into a new era on some automation-laden super-yacht while the rest of the world gets left behind with only oars and paddles.
It helped me realize how much of an oppurtunity there is for more widespread automation, 
and regret that it haven't been aware of a platform like Zapier sooner. 
What is the cost of not having this automation? What have we been missing out on? 

In talking to indepdent artists, I realized how many are spending hours a week on at least partially-automatable tasks. 
For example:

- posting and scheduling the same content across multiple platforms
- downscaling and watermarking images and video
- image-searching their artwork to protect against theft and misuse
- turning away spam accounts and requests for free art
- providing a streamlined commission-request system for potential clients

That's potentially hundreds of hours a year that each *each* artist is spending on *not* producing art.
And this does not just apply to indepedent artists, but any single-person or small business that primarily operates online.
I went through the initial trouble of automating my site's build, deployment, and LinkedIn notification steps
because I don't want some exciting idea I have for a post to be accompanied by repetitive barriers to its production,
just as I don't want an artist whose content I enjoy to have to face those same headwinds.

So I hope I have encouraged you to check out Zapier and other free-to-start automation platforms, 
or at least help spread the word to those that can benifit.
Access to automation extends a power that can go beyond simply saving time. 
I am excited to see what new things will be created, 
now that a long-neglected hurdle has been shortened so nearly anyone can jump over it.
