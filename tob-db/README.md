# TheOrgBook DB

## Overview

TheOrgBook DB is used to store the core Organizational data for searching (notably names, locations/addresses and claims held) and the claims themselves.

## Development

The DB component is an instance of Postgres. The schema and data loading is all handled by TheOrgBook API, and the Postgres image being used is an unchanged Red Hat image. As such, there is no build or database initialization associated with the DB - just the Deployment.

## Deployment

A set of shell scripts and OpenShift templates have been created to automate the process of configuring the OpenShift deployment resources for the DB.  The main scripts can be found in the **./openshift** folder.

### generateDeployments.sh

This script automates the process of configuring the OpenShift deployment environment for the DB.  You need to run this script against each of your deployment environments.

Use on Windows (from a Git Bash Shell):
```
	MSYS_NO_PATHCONV=1 ./generateDeployments.sh [project_namespace] [deployment_env_name] [build_env_name]
```

Example:
```
	MSYS_NO_PATHCONV=1 ./generateDeployments.sh devex-von dev tools
```

## ToDo:

- Nothing
