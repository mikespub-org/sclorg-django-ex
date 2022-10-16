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

