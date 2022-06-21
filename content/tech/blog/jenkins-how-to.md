Title: How I run my Jenkins cloud instance
Summary: Jenkins + helm template + kubectl apply -k
Date: 2022-06-20
Slug: jenkins-how-to

I have a few automation projects nearing the top of my to-do list
(there is a lot of repetitive work to do when you post and sell art online... yikes!),
so I recently dusted off [my rep's](https://github.com/exvertus/jenkins) to turn my personal Jenkins instance back on.
In updating it, I was reminded that it was a bit of process settling on a fully-declaritive solution I liked,
so I wanted to make a post about what I learned in case anyone finds themselves walking down the same path.

### Updating to the cloud

My Jenkins experience goes back to the non-containerized era,
when I was serving on a team that managed a company-wide "old-school" Jenkins instance.
When our machines neared capacity, our team would need to request a new VM, set it up manually, 
and ensure the proper dependencies were on the machine.
Moreover, the monolithic Jenkins would routinely be in "plugin-hell",
where so many plugins are installed to a single instance, they begin
necessitating lengthy review processes before we could "risk" running up-to-date plugin versions, nevermind updating the version of Jenkins itself, which would be perpetually spewing out warnings like "deprecated" and "not secure".

Knowing containers provided a code-managed way out of some of the 
traditional maintainence headaches, I used an oppurtunity I had supporting a smaller independent team to roll out a google cloud-friendly instance running on kubernetes, which had me quickly settling on [Helm](https://helm.sh/).

I'll gloss some of the additional details because this [youtube on 'The Jenkins Journey'](https://www.youtube.com/watch?v=IDoRWieTcMc&t=213s) will probably give you a better idea of how Jenkins will make a solution like Helm as its usage and needs grow.

### Helm is nice, but...

Helm, being a tool that writes and deploys to Kubernetes,
did make it easier to get Jenkins off the ground without having to know much Kubernetes, but customization quickly became a new bottleneck using it.

My existing experience configuring Jenkins started to make using Helm feel like putting the training wheels back on after already learning to ride a bike.
I could usually get it to do what I wanted *eventually*,
but it was too arduous to keep solving the "how do I do this through the Helm config?"
puzzle each time I needed to configure something new in Jenkins.

Moreover, what is Helm actually doing with the *Kubernetes config*?
Since the end k8s code Helm deploys doesn't exist in the repository,
there is no meaningful review process for Jenkins configuration 
changes unless another team member already knows what Helm will.
And wasn't a big reason I started down this path in the first place to
get all configuration into my versioned codebase?
While those are indirectly expressed in Helm's values.yaml file,
it really starts to feel more like a pseudo-declarative project using Helm.

### Kustomize is better

Thankfully a friend pointed me to a newer tool, kustomize.
I will again refer you [youtube](https://www.youtube.com/watch?v=WWJDbHo-OeY) for more details, 
but the TLDR is that kustomize lets me organize my project like this:
```
jenkins
├── helm-base ╍╍╍╍╷
└── overlays      ╎
    └── gke-tom ╍╍╵
```
In this case, my `helm-base` folder holds a yaml config of what Helm
*would* deploy if I was still using it as a package/deploy manager.
The line connecting that folder to `overlays/gke-tom` is showing that
gke-tom inherits from helm-base and *overlays* the gke-tom code over it,
essentially inserting and replacing fields in the configuration that
aren't specified or contain different values in helm-base.

So in less-technical terms, helm-base becomes "the rest of the world's best-pratice default yaml config" of Jenkins, and overlays can be thought of as "our deviation(s) from it". Since it is a yaml to yaml operation, I can keep stacking overlays on top of one another, like if I wanted to build a `helm-base > test > live` inheritence relationship, 
`helm-base > in-house-base > *multiple-in-house-jenkins-instances`, etc.

### Basic example on Google Kubernetes Engine
