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

*Note*: angular-scaffold no longer includes an nginx Build Configuration or Dockerfile.  These have moved to https://github.com/BCDevOps/openshift-tools/tree/master/images/nginx-runtime, and for those on the BC Gov Pathfinder platform, and image is available in the global `openshift` namespace so it is no longer necessary to build your own nginx image.

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

## Quick Start

A set of automation scripts have been wrapped around the project templates (described below) to make it quick and simple to deploy the OpenShift resources into an OpenShift environment such as the **`pathfinder.gov.bc.ca`** environment.

The scripts and templates have been configured to allow you to specify the GIT Repo, branch, and context directory for the builds.  This allows you to quickly redirect the build configurations to a different repository, branch, and folder structure.

_A word of caution… When deploying this application into a local cluster you will need to adjust the rules for the Nginx server, as they are preconfigured to only allow IP ranges that correspond to those in the `pathfinder.gov.bc.ca` environment._

### initializeProjects.sh

Use this script to initialize your project environments; assuming you are working with a standard `pathfinder.gov.bc.ca` OpenShift project set.

This script grants your deployment projects with access to pull images from your `tools` project.

Use:
```
./initializeProjects.sh <project-namespace> [tools-project-name:tools] [dev-project-name:dev] [test-project-name:test] [prod-project-name:prod]
```

Examples:

_Short Version:_
```
./initializeProjects.sh devex-von
```

_Full Version:_
```
./initializeProjects.sh devex-von tools dev test prod
```

#### generateBuilds.sh

Use this script to generate the build configurations for the project.

*NOTE:* This will *DELETE* all existing BuildConfigs and ImageStreams in the referenced OpenShift project.  If this is not what you want, you may process / apply the template output directly.

Use:
```
./generateBuilds.sh [project_name] [git_ref] [git_uri]
```

Example:
```
./generateBuilds.sh devex-von-tools master https://github.com/bcgov/TheOrgBook.git
```

### generateDeployments.sh

Use this script to generate the deployment configurations for the project.  You will need to run this script once for each of your deployment environments; dev, test, prod for example.

Use:
```
./generateDeployments.sh [project_namespace] [deployment_env_name] [build_env_name]
```

Example:
```
./generateDeployments.sh devex-von dev tools
```

## Template/Component Descriptions

This section provides additional details about the templates and their associated components.  It also provides instructions on how you would manually setup and configure the builds and deployments using the templates.  If you have used the scripts from the Quick Start section then you can ignore the manual setup and configuration instructions.

### (Manually) Set up angular-app BuildConfiguration

This is the s2i builder image that compiles the angular source code contained in your GitHub repo using OpenShift's NodeJS 6 image.

To add this image to your OpenShift Project:

1. Switch to the project where you wish to create the build configuration, e.g.:
  `oc project my-angular-project-tools`
1. Switch to the directory containing the angular app BuildConfiguration template:
  `cd openshift/templates/angular-app`
1. Process and import the results into the OpenShift project, providing appropriate parameter values:

  `oc process -f angular-app.json -p NAME=<name> -p GIT_REPO_URL=<your_repo> | oc create -f -`

  *Note:* Refer to `angular-app.json` for other available parameters.
  
  
What happens in OpenShift:
1. Fetches your angular code from <your_repo>
1. Executes source to image build strategy, processing your code based on contents of package.json and/or .s2i/bin/assemble
1. Pushes new image into your project's Image Streams with name of `<name>:latest`

### OPTIONAL: Setup Nginx-runtime

*NOTE:* This step is optional as there is a globally avaialbe nginx-runtime image in the `openshift` nanespace.  For simplicity teams may choose to use it.  If you wish to build your own `nginx-runtime` image, proceed with the steps in this section, otherwise you may skip.

This is a runtime image that is deployed with output of the `angular-builder`.

-update to latest mainline for every build.  If you need to pin it to a version alter the `nginx-runtime/Dockerfile`.

To add this image to your OpenShift Project,
1. Open OpenShift web console->Add to Project->Import YAML/JSON
1. Paste `nginx-runtime.json` into form -> Create
1. Change the Git Repo URL to yours -> Create
1. With the new build config, go to the Builds-> `nginx-runtime` -> Start Build

What happens in OpenShift:
1. Fetches `Dockerfile` from `<your repo>/angular-builder/Dockerfile`
1. Executes Dockerfile build strategy
1. Pushes new `nginx-runtime` image into your project's Image Streams

### Setup Angular-on-Nginx Builder

This is the s2i builder image that combinea the assembled output of `angular-builder` with the `nginx-runtime` image.  The result is a
new image based that will be be referenced in a DeploymentConfig and serve up your app's static front-end resources.

To add this image to your OpenShift Project,
1. Open OpenShift web console->Add to Project->Import YAML/JSON
1. Paste `angular-on-nginx-build.json` into form -> Create
1. Change the `Name` to the name of your application
1. Change the `Git Source Repo URL` to yours -> Create
1. This should auto trigger a build



To add this image to your OpenShift Project:

1. Switch to the project where you wish to create the build configuration, e.g.:
  `oc project my-angular-project-tools`
1. Switch to the directory containing the angular app BuildConfiguration template:
  `cd openshift/templates/angular-on-nginx`
1. Process and import the results into the OpenShift project, providing appropriate parameter values:

  `oc process -f angular-on-nginx-build.json -p NAME=<name> | oc create -f -`

  *Note:* Refer to `angular-app.json` for other available parameters.

What happens in OpenShift:
1. Copies output, i.e., `/opt/app-root/src/dist/` to `nginx-runtime` directory `tmp/app`
1. Pushed resulting  image, `<your app name>-build` to Image Stream

### Setup "Your App" Deployment

Once we've got an image out of the `angular-on-nginx` builder, e.g., `<your app name>`, we
need to setup the deployment.  We've provide a deployment template that is based on real load testing:
1. Tuned CPU/Memory for the nginx runtime on containers
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
1. Change the `Env TAG name` to the name of image tag you want this environment to listen for
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


