## Convert OpenShift templates to Helm charts

1. Download *template2helm* from https://github.com/redhat-cop/template2helm

2. Convert templates to charts

```
$ template2helm convert -t templates/webapp.json -c charts/
$ ...
```

3. Check format and package helm chart

```
$ helm lint --strict charts/webapp/
$ helm package charts/webapp/
$ ...
```

4. Create repository index

```
$ mv *.tgz ../docs/charts
$ cd ../docs
$ helm repo index --url https://github-org.mikespub.net/sclorg-django-ex/ .
```

For other issues, see https://www.qloudx.com/migrate-workloads-from-openshift-templates-to-helm-charts-part-1-of-3/

## Convert docker-compose files to OpenShift templates or Helm charts

1. Download *kompose* from https://github.com/kubernetes/kompose

2. Convert docker-compose file to OpenShift templates

```
$ kompose convert -o openshift/kompose --provider=openshift --build build-config
INFO Buildconfig using https://github.com/mikespub-org/sclorg-django-ex.git::flask-ex as source.
INFO OpenShift file "openshift/kompose/postgresql-service.yaml" created
INFO OpenShift file "openshift/kompose/web-service.yaml" created
INFO OpenShift file "openshift/kompose/postgresql-deploymentconfig.yaml" created
INFO OpenShift file "openshift/kompose/postgresql-imagestream.yaml" created
INFO OpenShift file "openshift/kompose/postgresql-claim0-persistentvolumeclaim.yaml" created
INFO OpenShift file "openshift/kompose/web-variables-env-configmap.yaml" created
INFO OpenShift file "openshift/kompose/web-deploymentconfig.yaml" created
INFO OpenShift file "openshift/kompose/web-imagestream.yaml" created
INFO OpenShift file "openshift/kompose/web-buildconfig.yaml" created
INFO OpenShift file "openshift/kompose/web-route.yaml" created
$ ...
```

3. Convert docker-compose file to Helm charts

```
$ kompose convert -c -o web-postgresql-kompose
INFO Kubernetes file "web-postgresql-kompose/templates/postgresql-service.yaml" created
INFO Kubernetes file "web-postgresql-kompose/templates/web-service.yaml" created
INFO Kubernetes file "web-postgresql-kompose/templates/postgresql-deployment.yaml" created
INFO Kubernetes file "web-postgresql-kompose/templates/postgresql-claim0-persistentvolumeclaim.yaml" created
INFO Kubernetes file "web-postgresql-kompose/templates/web-deployment.yaml" created
INFO Kubernetes file "web-postgresql-kompose/templates/web-variables-env-configmap.yaml" created
INFO Kubernetes file "web-postgresql-kompose/templates/web-ingress.yaml" created
INFO chart created in "web-postgresql-kompose/"
$ helm install flask-ex-helm web-postgresql-kompose
```

