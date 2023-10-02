Title: OWASP Dependency-Check for NodeJS
Summary: How to setup OWASP's open-source SCA automation on Google Cloud Build
Date: 2023-10-01 12:00
Category: Tech
Tags: how-to, security, cloud-build, owasp-depedency-check
Slug: owasp-dp-node

## It's 2023: do you know what's in your application?

Standing on the shoulders of giants is an important component in 
software development, 
and developers in higher-level languages become allergic to re-inventing wheels
for good reason. 
  
Chances are someone else has already encountered the same programming problem. 
Often there is an efficient solution encouraging good 
design patterns in the form of a code library, 
just waiting to be easily imported.

So relying heavily on upstream code has become second-nature because of the 
expressive power it lends by abstracting away complexity. 
Why spend the time and effort writing your own webserver, when you can simply
import Flask or Django and have a working webapp after a few minutes of coding?

The ubiquity of importing our way out of most programming problems means the 
vast majority 
of code that gets executed for a given application is *not* written 
or directly maintained by the same people responsible for developing that 
application. 
This is further exaserbated by the fact that most
dependencies have depedencies of their own, which can in turn have dependencies,
etc.
And a developer will mostly only be interested in the dependencies they 
directly import.

![Dependency Percent and Visibility](/images/posts/owasp-dp-node/dependencies.png)
  
I am as guilty as the next person of slapping together projects by mostly
importing open-source libraries found reading doc and searching StackOverflow.
I did it for years serving in a SDLC-automation role, and while I do miss
those more naive wild-west years (security was a total after-thought 
and we only worried about making it work and it not running up the cloud bill!)
those days are unfortunately long gone...

## Software supply-chain attacks are already here to stay

I recently wrapped up a six-month contract serving in a cyber-security role.
In the process of getting ready for the role, I was shocked to learn how common 
these dependencies have been used to deliver deeply-buried exploitable code.
In the AppSec world, these are called **supply chain attacks**, and they seem
to be getting more sophisticated and common every day:

* [Help Net Security: Supply chain attacks caused more data compromises than malware](https://www.helpnetsecurity.com/2023/01/26/data-compromises-2022/)
* [CSO: Supply chain attacks increased over 600% this year and companies are falling behind](https://www.csoonline.com/article/573925/supply-chain-attacks-increased-over-600-this-year-and-companies-are-falling-behind.html)
* [Wired: A New Supply Chain Attack Hit Close to 100 Victims—and Clues Point to China](https://www.wired.com/story/carderbee-china-hong-kong-supply-chain-attack/)

Even when not intentional, zero-day vulnerabilities like 
[Heartbleed](https://en.wikipedia.org/wiki/Heartbleed), 
[Cloudbleed](https://en.wikipedia.org/wiki/Cloudbleed),
and [Log4j](https://en.wikipedia.org/wiki/Log4Shell) often lie dormant
in systems for years, waiting to be exploited.

So how can we know whether to trust an imported software library?
Well, we could review every single line of a given dependency ourselves.
But going to that extreme takes away all the complexity-abstraction value,
and will have us feeling like are in 
[one of Borges' short stories](https://en.wikipedia.org/wiki/On_Exactitude_in_Science).
While it is not feasible to eliminate all vulnerabilities, there is an 
open-source solution to quickly scan an application for dependencies with 
*known* vulnerabilities.

## OWASP Dependency-check







I. Introduction
Briefly introduce OWASP Dependency-Check.
Explain the importance of Software Composition Analysis (SCA).
Introduce Google Cloud Build.
Brief overview of what the post will cover.

II. The Problem
Discuss the issues with managing dependencies.
Explain the risks of using outdated or vulnerable dependencies.
Highlight the need for automated tools to manage dependencies.

III. The Solution: OWASP Dependency-Check
Discuss the features and benefits of OWASP Dependency-Check.
Explain how it can be used for Node.js projects.

IV. Setting Up OWASP Dependency-Check on Google Cloud Build
A. Prerequisites
css
Copy code
  - Explain what the reader needs to follow along (Google Cloud account, Node.js project, etc.)
B. Step-by-Step Guide
vbnet
Copy code
  - Step 1: Configuring the Google Cloud Build.
  - Step 2: Integrating OWASP Dependency-Check into the build pipeline.
  - Step 3: Configuring OWASP Dependency-Check for a Node.js project.
  - Step 4: Reviewing and addressing the scan results.
C. Tips and Best Practices
sql
Copy code
  - Offer tips and best practices for working with OWASP Dependency-Check and Google Cloud Build.

VI. Conclusion
Summarize the main points.
Encourage readers to integrate OWASP Dependency-Check in their Google Cloud Build pipelines for Node.js projects.

VII. Further Resources
Provide links to the OWASP Dependency-Check documentation, Google Cloud Build documentation, and other relevant resources.

VIII. Contact Information
Provide contact information for readers who have questions or need further assistance.
