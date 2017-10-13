# TheOrgBook API

## Overview

The API provides an interface into the database for TheOrgBook.

## Development

The API is developed in Django/Python, using a Visual Studio 2017 project.

## Deployment

A set of shell scripts and OpenShift templates have been created to automate the process of configuring the OpenShift build and deployment resources for the API.  The main scripts can be found in the **./openshift** folder.

### generateBuilds.sh

This script automates the process of configuring the OpenShift build environment for the API project.

Use on Windows (from a Git Bash Shell):
```
	MSYS_NO_PATHCONV=1 ./generateBuilds.sh [project_name] [git_ref] [git_uri]
```

Example:
```
	MSYS_NO_PATHCONV=1 ./generateBuilds.sh devex-von-tools master https://github.com/bcgov/TheOrgBook.git
```

### generateDeployments.sh

This script automates the process of configuring the OpenShift deployment environment for the API project.  You need to run this script against each of your depoyment environments.

Use on Windows (from a Git Bash Shell):
```
	MSYS_NO_PATHCONV=1 ./generateDeployments.sh [project_namespace] [deployment_env_name] [build_env_name] 
```

Example:
```
	MSYS_NO_PATHCONV=1 ./generateDeployments.sh devex-von dev tools
```

## Development Deployment Environment

- [Schema Spy](http://schema-spy-devex-von-dev.pathfinder.gov.bc.ca/)
- [Open API (Swagger) API Explorer](http://devex-von-dev-django.pathfinder.gov.bc.ca/api/v1/)

## Database Migrations

Migrations are triggered automatically when the Django/Python container is deployed.  The process it triggered by wrapper code injected as part of the s2i-python-container build; https://github.com/sclorg/s2i-python-container/blob/master/3.6/s2i/bin/run

## ToDo:
- The auto-generated views are constructed using generics and a number of mixins.
  - Determine if there is a better way to do this.  Since it's not as clean as something constructed from ModelSerializer or HyperlinkedModelSerializer.
- Logging; ref gwells