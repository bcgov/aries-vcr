# OpenShift and Jenkins Integration
This documentation provides you with step by step instructions on how to build and deploy this 
application in an OpenShift 3.3+ and Jenkins 2.x+ environment.  Jenkins is not required and you could 
just use the built-in OpenShift triggers.

The benefits are:

- Uses Nginx to serve static files (10x faster than NodeJS)
- Only build outputs are on runtime container (reduces security risk and container size)
- Uses `mainline` nginx to automatically keep up with patches
- (Optional) configure Nginx as a reverse proxy for REST APIs

Enhancements to base Nginx image are:

- security response HTTP headers
- throttling to reduce DDoS
- W3C standard log formatting
- performance tuning
- uses X-Forwarded-For for client IP for better logging and access control.
- gzip enabled for better client performance
- Optional IP filtering for access control
- Optional HTTP Basic for simple access control 

## Overview

This build strategy uses OpenShift's feature called [Extended Builds](https://docs.openshift.com/container-platform/3.3/dev_guide/builds.html#extended-builds).

In a nutshell, it allows you to build with one s2i image, i.e., NodeJS 6+, then use another image, i.e., nginx, for runtime.

OpenShift is responsible for:
- Building Docker images
- Building S2I Images
- Moving output of S2I to runtime image
- Deployments

Jenkins is responsible for:
- Listening for pushes from GitHub SCM, i.e., GitHub hook -> Jenkins
- Triggers the Build/Deploy Pipeline
- Executing the `Jenkinsfile`
  - SCM checkout
  - Trigger OpenShift to build images
  - Tagging images to instruct OpenShift to deploy
- Build notifications, repo tagging and other CI/CD goodies

## Setup Angular-Builder

This is your builder image that compiles the angular source code.

This image is based on the OpenShift's community NodeJS 6 image, i.e., `FROM centos/nodejs-6-centos7`.
We use this because the stock NodeJS 4 can't compile `angular-cli` (an ES6 issue).  Once the stock NodeJS 4 image
is upgraded this won't be required.

To add this image to your OpenShift Project,
1. Open OpenShift web console->Add to Project->Import YAML/JSON
1. Paste `angular-builder.json` into form -> Create
1. Change the Git Repo URL to yours -> Create
1. With the new build config, go to the Builds-> `angular-builder` -> Start Build

What happens in OpenShift:
1. Fetches `Dockerfile` from `<your repo>/angular-builder/Dockerfile`
1. Executes Dockerfile build strategy
1. Pushes new `angular-builder` image into your project's Image Streams

## Setup Nginx-runtime

This is your runtime image that is deployed with output of the `angular-builder`.

This images is based on docker hub's official nginx image, i.e., `FROM nginx:mainline`.  It will auto
update to latest mainline for every build.  If you need to pin it to a version alter the `nginx-runtime/Dockerfile`.
  
To add this image to your OpenShift Project,
1. Open OpenShift web console->Add to Project->Import YAML/JSON
1. Paste `nginx-runtime.json` into form -> Create
1. Change the Git Repo URL to yours -> Create
1. With the new build config, go to the Builds-> `nginx-runtime` -> Start Build

What happens in OpenShift:
1. Fetches `Dockerfile` from `<your repo>/angular-builder/Dockerfile`
1. Executes Dockerfile build strategy
1. Pushes new `nginx-runtime` image into your project's Image Streams

## Setup Angular-on-Nginx Builder

This is the s2i builder image to glue the `angular-builder` output with the `nginx-runtime` image.  The result is a
new image based on `nginx-runtime` but with the output of `angular-builder`.

To add this image to your OpenShift Project,
1. Open OpenShift web console->Add to Project->Import YAML/JSON
1. Paste `angular-on-nginx-build.json` into form -> Create
1. Change the `Name` to the name of your application
1. Change the `Git Source Repo URL` to yours -> Create
1. This should auto trigger a build

What happens in OpenShift:
1. Trigger's `angular-builder` to build with your source code
1. Copies output, i.e., `/opt/app-root/src/dist/` to `nginx-runtime` directory `tmp/app`
1. Create to image, `<your app name>-build` to Image Stream

## Setup "Your App" Deployment

Once we've got an image out of the `angular-on-nginx` builder, e.g., `<your app name>`, we
need to setup the deployment.  We've provide a deployment template that is based on real load testing:
1. Tuned CPU/Memory for the ngnix runtime on containers
1. Auto-scaling for high work loads
1. Tweaked readiness and liveness probes settings

The deployment template will create in OpenShift:
1. Deployment config with default nginx runtime env vars
1. Service config
1. Route config

To add this image to your OpenShift Project,
1. Open OpenShift web console->Add to Project->Import YAML/JSON
1. Paste `angular-on-nginx-deploy` into form -> Create
1. Change the `Name` to the name of your application
1. Change the `Image Namespace` to the project of where it's built
1. Change the `Env TAG name` to the name of your application
1. Change the `APPLICATION_DOMAIN` to the domain name you would like
1. This should auto trigger a build

Repeat these steps for each environment you have changing the `Env TAG name`.

## Jenkins vs OpenShift Triggers

You can choose not to use Jenkins at this point.  Instead, use vanilla OpenShift build triggers and image
changes deployments.  However, Jenkins provides some nice features you'll probably need.

## Jenkins Install

So, you've chosen to use Jenkins!  Congrats!
  
This repo also comes with a `Jenkinsfile` to take advantage of the Pipelines feature in OpenShift and Jenkins.

[Follow BCDevOps Jenkins Configuration to get started](https://github.com/BCDevOps/issues-and-solutions/wiki/Jenkins-Configuration)

Note: we've already provided the default `Jenkinsfile` tailored for this app.

## Jenkins Additional Setup

Jenkins out-of-the-box needs some additional setup.  

1. First off, you'll need the admin password.  Go the Deployments -> `jenkins-pipeline-svc` -> Environment -> `JENKINS_PASSWORD`
1. Navigate to jenkins web site by looking in your Routes in made for Jenkins
1. Upgrade all the plugins in Jenkins
1. Add GitHub webhook to GitHub from OpenShift Web Console->Pipelines->Edit <something>-pipeline->GitHub webhooks 

## Jenkins Manual Setup

You can also create a Job in Jenkins and point your Job to the Jenkinsfile.   


