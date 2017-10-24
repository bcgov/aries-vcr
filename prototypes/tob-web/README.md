# TheOrgBook Web

## Overview

The Web implements the user interface for TheOrgBook, calling the API to manage data. The interface is served from an instance of [NGINX](https://www.nginx.com/).

## Development

The Web is developed in Angular-4, and is based on the [BC Gov Angular Scaffold](https://github.com/bcgov/angular-scaffold) Starter Kit. See the [instructions](./Angular-Development.md) in the file ./Angular-Development.md for more information about running locally and developing with Angular 4.

## Deployment

A set of shell scripts and OpenShift templates have been created to automate the process of configuring the OpenShift build and deployment resources for the Web.  The main scripts can be found in the **./openshift** folder.

### generateBuilds.sh

This script automates the process of configuring the OpenShift build environment for the Web images.

Use on Windows (from a Git Bash Shell):
```
	MSYS_NO_PATHCONV=1 ./generateBuilds.sh [project_name] [git_ref] [git_uri]
```

If you are building a local environment - use the URL for your own fork of the github repo vs. the BC Gov repo in the following command.

Example:
```
	MSYS_NO_PATHCONV=1 ./generateBuilds.sh devex-von-tools master https://github.com/bcgov/TheOrgBook.git
```

The builds are not (currently) triggered by the generateBuilds.sh command, so this must be done manually:

```
oc project devex-von-tools;
oc start-build angular-builder;
oc start-build angular-pipeline;
```

### generateDeployments.sh

This script automates the process of configuring the OpenShift deployment environment for the API project.  You need to run this script against each of your deployment environments.

Use on Windows (from a Git Bash Shell):
```
	MSYS_NO_PATHCONV=1 ./generateDeployments.sh [project_namespace] [deployment_env_name] [build_env_name]
```

Example:
```
	MSYS_NO_PATHCONV=1 ./generateDeployments.sh devex-von dev tools
```

## ToDo:

- Add the triggering of the initial builds on running generateBuilds.sh
