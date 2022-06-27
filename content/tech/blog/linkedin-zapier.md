Title: Zapier automation for LinkedIn posts
Summary: Automation 'for the little guy' can have a big impact
Date: 2022-06-26
Tags: tech, how-to, linkedin, automation, zapier
Slug: linkedin-zapier

I recently configured a bit of personal automation for myself,
and if you arrived here via my blogpost share on LinkedIn,
you've already used it.
I not only wanted to share how easy it was to configure it with Zapier,
but also why I am extremely excited that a dream of widepread accessibility to
software automation is already becoming a reality today.

### Why automate?

As someone with a more than a few absent-minded-professor tendencies,
I knew that posting to my LinkedIn manually would quickly fall to pieces.
While things like avoiding manual errors and not having to remember each time are welcome benefits, I always like to emphasize my biggest reason for automating:

*The less something costs to create, the more it will be produced.*

While few disagree with the statement in theory,
the temptation to forget in practice is very real.
I admit I 'kick the can' too often myself 
(the current lose ends in this site's repo provides a case-in-point), 
but when each productive iteration requires an arduous process that is left unchecked, a feeling of dread begins to get coupled to the creation process.
It can become so internalized that it is shrugged off as an "given" to producing whatever could come next.

Without process improvements this can quickly give rise to a lethargic creative depression: new ideas increasingly fall under the shadow of 'too much of a bother'. Ideas carrying the potency to be the next big breakthrough are ironically rejected for their potential to 'open a Pandora's box'.
I have seen first hand how much this can hollow-out a software development team's productivity, but much has already been said about the impact technical debt creates in a corporate setting and the stand-stills it can usher in if not take seriously.
I do not dismiss that debate as much as want stay focused on something much closer to my heart of late---enabling automation for the *individual*.

A proliferation of automation accessibility can solve some big problems we might not even be fully aware we have, but I will try to connect the dots on that broader and more speculative assertion below. That will be easier to do if I first show you how easy automation has helped me personally in more recent and concrete terms: automatically sharing to my LinkedIn each time I publish a new post on my site (like this one).

### How automation usually goes

So I started the process as many others with experience in the software automation world would:
1. Review the [API documentation](https://docs.microsoft.com/en-us/linkedin/) to ensure the data I require for my automation is available via public endpoint(s) in the first place.
2. Search for an existing API-client that wraps things like authentication and endpoint calls in my preferred programming language.
3. Import and use the existing API-client if it is available, otherwise write a minimal implementation of one myself.

Step 1 was easy enough. 
LinkedIn does indeed provide an [API path](https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin#creating-a-share-on-linkedin) enabling automatic sharing, including my need to [share a url](https://docs.microsoft.com/en-us/linkedin/consumer/integrations/self-serve/share-on-linkedin#create-an-article-or-url-share).

Step 2 is where things got messy.
First I found a [python-linkedin lib](https://github.com/ozgur/python-linkedin) that looked promising, until I noticed the last update was in 2015, a year before Microsoft acquired LinkedIn. No thanks.

Next I found the more current [linkedin-api](https://github.com/tomquirk/linkedin-api). It initially seemed promising until I looked closer for how to share and could not find one. This library leans on an alternative service for its endpoints called Voyager and it looks like the share endpoint [has not been exposed](https://github.com/tomquirk/linkedin-api/issues/106) in the python lib yet. I initially tried to add the feature myself, but after going well down the path of forking the repo, configuring a dev build, setting up an account for the .env file, getting the tests (which make requests to the live server while also using a timer-delay to prevent throttling, resulting in minutes-long test runs) to pass, and looking at the code, I started to question all the time I was spending to add a fairly simple feature to a python project screaming for a refactor. So I went to sleep that night thinking I would be writing a minimal python client-wrapper in a utils directory of my site's repository in order to call it from a new post-step in my Jenkinsfile after a successfull build-deploy from the 'main' branch.

If I lost you because of the technical mumbo-jumbo, that was kind of the point. In fact, you can forget everything from this section except this part: that *building and configuring this automation gets very complicated very quickly*. That fact is a key to understanding a problem I have been increasingly concerned with, but that a platform I just discovered named Zapier is already fixing. Sorry for the technical derailment. Keep reading.

### Discovering Zapier

It felt fitting that I should taste some of the discouragement that keeps automation prohibitive for most, and perhaps the frustration was the necessary motivation for getting myself out of the professional-software-automator box enough to find Zapier.


TODO: what does sharing the Zap do?
Share how-to and that you had to adjust plugin for RSS
Easy to configure and test with real data

### Automation Democratization? It's *about time*...

...and not just about saving people more of it. It's about time automation become widely available because of what we've *all* been missing out on.

I'll repeat the axiom I opened with here: *the less something costs to create, the more it will be produced*.

If you share my interest in economics, you may have already guessed at the inspiration for this axiom: "if you want more of something, subsidize it" and the inverse, "if you want less of something, tax it".
You may recall a similar price-control phenomenon,
where effective price-floors tend towards surpluses, and shortages tend to follow price-caps. It will help to similarly hold the inverse in mind: the *more* something costs to create, the *less* it will be produced.

Actually running most automation is usually not costly. The true cost comes in the complexity I gave you a taste of above, which is also reflected in the cost of hiring a software engineer. When I moved to Austin I began meeting other indpendent artists and talked to a few owners of small creative businesses around town. Contrasting their utilization of automation against my time building it for years in the corporate tech industry, it felt like that industry sailed into the next era on some automation-laden super-yacht while the rest of the world gets left behind.

I focused on the art world because it is near and dear, but when you consider who else 'left behind' includes, it gets more concerning:  

Now you can understand why I have increasingly come to feel urgency towards automation availability. I fear the oppurtunity costs. What have we been missing out on? The best answer I can muster is "better something". What exactly could be better, and by how much, cannot be measured until *after* focused creative souls have had the chance to transform their original idea into reality.


artists left behind when it comes to automation
applies to ALL 1-person businesses and side-hustles
where is the market for this?

 but getting back to my own needs, I went through the initial trouble of automating my site's build,
deployment, and follow-up-on-LinkedIn notification step,
because I don't want some exciting idea I have for a future post to be
accompanied by potential barriers to its production.
I want to feel like I can run with an idea without having
to determine if its realization clears some neglected hurdle to determine if it is "worth it".

 is that if I don't, 
there probably won't be a site for very much longer.
