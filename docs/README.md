# Mike's Pub Helm Charts
This repository contains the helm charts for the Flask version of sclorg/django-ex in the OpenShift Developer Catalog

The repository has been configured to serve the static helm index and chart files

## Usage

```

$ helm repo add mikespub-charts https://github-org.mikespub.net/sclorg-django-ex/
"mikespub-charts" has been added to your repositories

$ helm repo list 
NAME           	URL                               
mikespub-charts	https://github-org.mikespub.net/sclorg-django-ex/

$ helm search repo mikespub-charts
NAME                                 	CHART VERSION	APP VERSION	DESCRIPTION
mikespub-charts/postgresql-persistent	v0.0.1       	           	PostgreSQL database service, with persistent st...
mikespub-charts/robot-template       	v0.0.1       	           	Template to create '${NAME}' service account wi...
mikespub-charts/webapp               	v0.0.1       	           	Flask application with a PostgreSQL database. F...

$ helm show values mikespub-charts/webapp | grep TODO > webapp-values.yaml
$ vi webapp-values.yaml
...
$ helm install -f webapp-values.yaml webapp-release mikespub-charts/webapp
...

$ helm list
NAME       	NAMESPACE   	REVISION	UPDATED                                	STATUS  	CHART        	APP VERSION
...
$ helm get all webapp-release
NAME: webapp-release
...

$ helm uninstall webapp-release
...
```


## Helm index

https://github-org.mikespub.net/sclorg-django-ex/index.yaml
 

## Source repository

https://github.com/mikespub-org/sclorg-django-ex


## [How To Submit a New Chart](https://github.com/redhat-developer/redhat-helm-charts/wiki/Adding-a-New-Chart)

Source: https://github.com/redhat-developer/redhat-helm-charts
