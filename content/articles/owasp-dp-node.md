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
This is further exacerbated by the fact that most
dependencies have dependencies of their own, which can in turn have dependencies,
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

## OWASP Dependency-check how-to

In light of this situation, 
I wanted to share how I recently added 
[OWASP Dependency-check](https://owasp.org/www-project-dependency-check/) 
automation to a project, and how easy it was.

The project is a NodeJS discord bot that my friends and I maintain and deploy 
onto a shared GKE instance.
While we have kept it mostly up-to-date,
it has sprawled out to include quite a few features over the years,
and we're now relying on quite a few dependencies to run the project.

The first thing I needed to do was add one more dev dependency to our 
package.json file, as well as an entrypoint to the OWASP call:

```
# /package.json
{
  "name": "darnbot",
  ...
  "scripts": {
    "owasp": "owasp-dependency-check --project darnbot -f HTML -f JSON -o owasp",
    ...
  },
  "devDependencies": {
    "owasp-dependency-check": "^0.0.21",
    ...
  }
}
```

The new "scripts" line will allow us to call 'npm run owasp' to start the scan,
with the requested HTML and JSON artifacts dropped in an 'owasp' folder, 
specified by the -o argument.

Now onto the [Cloud Build](https://cloud.google.com/build?hl=en) code, which I
split off into a separate file from our [normal cloudbuild.yaml](https://cloud.google.com/build/docs/configuring-builds/create-basic-configuration#yaml) file.
I wanted to do it this way to run manually for now, until we are ready for
more integrated automation in our pipeline triggered by changes to main:

```
# /owasp-dp.yaml
steps:
- id: 'install'
  name: 'node:${_NODE_VERSION}'
  entrypoint: 'npm'
  args: ['install']
- id: 'owasp'
  name: 'node:${_NODE_VERSION}'
  script: |
    apt-get update
    apt-get install -y default-jre
    npm run owasp
artifacts:
  objects:
    location: gs://$_ARTIFACT_BUCKET
    paths: ['owasp/dependency-check-report.html','owasp/dependency-check-report.json']
```

After using a [substitution](https://cloud.google.com/build/docs/configuring-builds/substitute-variable-values)
to feed in our node version, we install our code to a serverless node container.
After which, the 'npm run owasp' is called.

One minor wrinkle I ran into is because we use a light-weight container 
to run our bot, it was necessary to install the default jre in order to handle 
java calls that OWASP Dependency-check required.
Installing java each time is fine for now since this is only run on-demand,
but before incorporating this into our main branch's cloudbuild.yaml,
I would move the apt-get lines to a second Dockerfile inheriting our
built image so it is not needlessly installed for every change to main.

Under artifacts you can see we are taking the html and json reports and
saving them to a Google Cloud Storage bucket.

Finally, in order to run the automation, we need to add a trigger through the
GCP UI:

![Cloud Build UI](/images/posts/owasp-dp-node/cloud-build.png)

After configuring and saving, GCP creates a build with a 'Run' button on the
Build Triggers page so we can run the build:

![Cloud Build Run](/images/posts/owasp-dp-node/cloud-build-run.png)

![Cloud Build Steps](/images/posts/owasp-dp-node/cloud-build-steps.png)

Jumping over to the Storage bucket, we can take a look at the HTML results.
Looks like we've got a bit of work to do:

![Summary of results](/images/posts/owasp-dp-node/owasp-results.png)

If you set this up for yourself, you'll be able to view more detail
about each detected vulnerability farther down the page.
I have cut off our specific vulnerabilities for obvious reasons.

## Conclusion

VI. Conclusion
Summarize the main points.
Encourage readers to integrate OWASP Dependency-Check in their Google Cloud Build pipelines for Node.js projects.

VIII. Contact Information
Provide contact information for readers who have questions or need further assistance.
