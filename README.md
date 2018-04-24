# Openshift quickstart: Flask

This is a [Flask](http://flask.pocoo.org/) project that you can use as the starting point to develop your own and deploy it on an [OpenShift](https://github.com/openshift/origin) cluster.

The steps in this document assume that you have access to an OpenShift deployment that you can deploy applications on.

## What has been done for you

This is a minimal Flask `0.12.2` project. It was created with these steps:

1. Create a virtualenv
2. Manually install Flask and other dependencies
3. Load automatically all the env variables starting with `APP_`
3. `pip freeze > requirements.txt`
3. Configure `SECRET_KEY`, `DB_NAME`, `DB_USER`, `DB_PORT`, `DB_SERVICE_NAME`, `DB_ENGINE` and `FLASK_APP` entries
4. Display a hello world with some info

From this initial state you can:
* continue the development of your Flask project
* update settings to suit your needs
* install more Python libraries and add them to the `requirements.txt` file

## Special files in this repository

Apart from the regular files  (`app/`, `wsgi.py`), this repository contains:

```
openshift/         - OpenShift-specific files
└── templates      - application templates

requirements.txt   - list of dependencies
```

## Warnings

Please be sure to read the following warnings and considerations before running this code on your local workstation, shared systems, or production environments.

### Database configuration

The sample application code and templates in this repository contain database connection settings and credentials that rely on being able to use sqlite.

### Automatic test execution

The sample application code and templates in this repository contain scripts that automatically execute tests via the postCommit hook.  These tests assume that they are being executed against a local test sqlite database. If alternate database credentials are supplied to the build, the tests could make undesireable changes to that database.

## Local development

To run this project in your development machine, follow these steps:

1. (optional) Create and activate a [virtualenv](https://virtualenv.pypa.io/) (you may want to use [virtualenvwrapper](http://virtualenvwrapper.readthedocs.org/)).

2. Ensure that the executable `pg_config` is available on your machine. You can check this using `which pg_config`. If not, install the dependency with one of the following.
  - macOS: `brew install postgresql` using [Homebrew](https://brew.sh/)
  - Ubuntu: `sudo apt-get install libpq-dev`
  - [Others](https://stackoverflow.com/a/12037133/8122577)

3. Fork this repo and clone your fork:

    `git clone https://github.com/renefs/flask-ex.git`

4. Install dependencies:

    `pip install -r requirements.txt`

6. If everything is alright, you should be able to start the Flask development server:

    `FLASK_APP=wsgi.py flask run`

7. Open your browser and go to `http://127.0.0.1:5000`, you will be greeted with a welcome page.


## Deploying to OpenShift

To follow the next steps, you need to be logged in to an OpenShift cluster and have an OpenShift project where you can work on.


### Using an application template

The directory `openshift/templates/` contains OpenShift application templates that you can add to your OpenShift project with:

    oc create -f openshift/templates/<TEMPLATE_NAME>.json

The template `flask.json` contains just a minimal set of components to get your Flask application into OpenShift.

The template `flask-postgresql.json` contains all of the components from `flask.json`, plus a PostgreSQL database service and an Image Stream for the Python base image. For simplicity, the PostgreSQL database in this template uses ephemeral storage and, therefore, is not production ready.

After adding your templates, you can go to your OpenShift web console, browse to your project and click the create button. Create a new app from one of the templates that you have just added.

Adjust the parameter values to suit your configuration. Most times you can just accept the default values, however you will probably want to set the `GIT_REPOSITORY` parameter to point to your fork and the `DATABASE_*` parameters to match your database configuration.

Alternatively, you can use the command line to create your new app, assuming your OpenShift deployment has the default set of ImageStreams defined.  Instructions for installing the default ImageStreams are available [here](https://docs.openshift.org/latest/install_config/imagestreams_templates.html).  If you are defining the set of ImageStreams now, remember to pass in the proper cluster-admin credentials and to create the ImageStreams in the 'openshift' namespace:

    oc new-app openshift/templates/flask.json -p SOURCE_REPOSITORY_URL=<your repository location>

Your application will be built and deployed automatically. If that doesn't happen, you can debug your build:

    oc get builds
    # take build name from the command above
    oc logs build/<build-name>

And you can see information about your deployment too:

    oc describe dc/flask-example

In the web console, the overview tab shows you a service, by default called "flask-example", that encapsulates all pods running your Flask application. You can access your application by browsing to the service's IP address and port.  You can determine these by running

    oc get svc


### Without an application template

Templates give you full control of each component of your application.
Sometimes your application is simple enough and you don't want to bother with templates. In that case, you can let OpenShift inspect your source code and create the required components automatically for you:

```bash
$ oc new-app centos/python-35-centos7~https://github.com/renefs/flask-ex
imageStreams/python-35-centos7
imageStreams/flask-ex
buildConfigs/flask-ex
deploymentConfigs/flask-ex
services/flask-ex
A build was created - you can run `oc start-build flask-ex` to start it.
Service "flask-ex" created at 172.30.16.213 with port mappings 8080.
```

You can access your application by browsing to the service's IP address and port.


## Logs

By default your Flask application is served with gunicorn and configured to output its access log to stderr.
You can look at the combined stdout and stderr of a given pod with this command:

    oc get pods         # list all pods in your project
    oc logs <pod-name>

This can be useful to observe the correct functioning of your application.


## Special environment variables

### APP_CONFIG

You can fine tune the gunicorn configuration through the environment variable `APP_CONFIG` that, when set, should point to a config file as documented [here](http://docs.gunicorn.org/en/latest/settings.html).

### APP_SECRET_KEY

When using one of the templates provided in this repository, this environment variable has its value automatically generated. For security purposes, make sure to set this to a random string as documented [here](https://docs.djangoproject.com/en/1.8/ref/settings/#std:setting-SECRET_KEY).


## One-off command execution

At times you might want to manually execute some command in the context of a running application in OpenShift.

You can do all that by using regular CLI commands from OpenShift.

Here is how you would run a command in a pod specified by label:

1. Inspect the output of the command below to find the name of a pod that matches a given label:

        oc get pods -l <your-label-selector>

2. Open a shell in the pod of your choice. Because of how the images produced
  with CentOS and RHEL work currently, we need to wrap commands with `bash` to
  enable any Software Collections that may be used (done automatically inside
  every bash shell).

        oc exec -p <pod-name> -it -- bash

3. Finally, execute any command that you need and exit the shell.

Related GitHub issues:
1. https://github.com/GoogleCloudPlatform/kubernetes/issues/8876
2. https://github.com/openshift/origin/issues/2001


## Data persistence

You can deploy this application without a configured database in your OpenShift project, in which case Flask will use a temporary SQLite database that will live inside your application's container, and persist only until you redeploy your application.

After each deploy you get a fresh, empty, SQLite database. That is fine for a first contact with OpenShift and perhaps Flask, but sooner or later you will want to persist your data across deployments.

To do that, you should add a properly configured database server or ask your OpenShift administrator to add one for you. Then use `oc env` to update the `DATABASE_*` environment variables in your DeploymentConfig to match your database settings.

Redeploy your application to have your changes applied, and open the welcome page again to make sure your application is successfully connected to the database server.


## Looking for help

If you get stuck at some point, or think that this document needs further details or clarification, you can give feedback and look for help using the channels mentioned in [the OpenShift Origin repo](https://github.com/openshift/origin), or by filing an issue.


## License

This code is dedicated to the public domain to the maximum extent permitted by applicable law, pursuant to [CC0](http://creativecommons.org/publicdomain/zero/1.0/).
