# Tom's site

Infrastructure and content for my personal site [thomasflanigan.com](https://thomasflanigan.com).

* Built with [hugo](https://gohugo.io/)
  * Run ```hugo serve -D``` from repo root to run local live server
  * Use ```hugo --cleanDestinationDir``` to build static files
* Running on [nginx](https://www.nginx.com/) webserver
* Hosted on [GKE](https://cloud.google.com/kubernetes-engine)
  * Deploy with ```cat k8s-config.yaml | envsubst | kubectl apply -f -```