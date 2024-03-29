# Tom's site

Infrastructure and content for my personal site [thomasflanigan.com](https://thomasflanigan.com).

* Built with [Pelican](https://blog.getpelican.com/)
  * Build: ```make html```
  * Run local: ```make devserver```
* Running on [nginx](https://www.nginx.com/) webserver
  * Build Dockerfile with ```docker build -t $TOMS_SITE_IMG .```
  * And push ```docker push $TOMS_SITE_IMG```
* Hosted on [GKE](https://cloud.google.com/kubernetes-engine)
  * Deploy with ```cat k8s-config.yaml | envsubst | kubectl apply -f -```
  * Test service with ```kubectl port-forward service/site-svc -n thomasflanigan 8080:8080 >> /dev/null```
