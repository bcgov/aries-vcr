# TheOrgBook DB

## Overview

TheOrgBook DB is used to store the core Organizational data for searching (notably names, locations/addresses and claims held) and the claims themselves.

## Development

The DB component is an instance of Postgres. The schema and data loading is all handled by TheOrgBook API, and the Postgres image being used is an unchanged Red Hat image. As such, there is no build or database initialization associated with the DB - just the Deployment.

## Deployment

To deploy TheOrgBook on an instance of OpenShift, see [the instructions](../RunningLocal.md) in the file RunningLocal.md.

# BC Registries DB

## Overview

Internally TheOrgBook connects to an instance of the BC registries database (Oracle) via an a PostgreSQl database via oracle_fdw.

Refer to [Oracle-fdw-Testing](Oracle-fdw-Testing.md) for information on configuration and testing the connection.

# Database Schema Documentation

Databases are documented using [SchemaSpy](https://github.com/bcgov/SchemaSpy).  The documentation of the Oracle database requires Oracle JDBC drivers.  Due to licensing restrictions the image for the associated pod has been built manually and pushed into the project's tools project.

## BC Registries SchemaSpy Instance (schema-spy-oracle)

This instance is protected by basic authentication.  The credentials are randomly generated for each deployment.

To accomplish this, we use a little bit of OpenShift magic.  We use a combination of config maps and secrets to inject a customized Caddy configuration file into the running SchemaSpy instance and define the set of credentials used for basic authentication.  To orchestrate and automate the process we use features of the [OpenShift Scripts](https://github.com/BCDevOps/openshift-project-tools/blob/master/bin/README.md) used to setup and maintain OpenShift environments.

The [schema-spy-oracle-deploy](./openshift/templates/schema-spy-oracle-deploy.json) template performs most of the heavy lifting.  It defines the nesessary plumbing to mount the custom Caddy configuration into a running SchemaSpy instance and defines the secrets to hold the credentials, along with some additional SchemaSpy settings to redirect the output to the correct folder.

The custom [Caddyfile](./openshift/templates/Caddyfile) defines the routes and basic authentication that allow OpenShift to perform health checks while protecting the database documentation.

The [schema-spy-oracle-deploy.overrides.sh](./openshift/schema-spy-oracle-deploy.overrides.sh) script generates the configuration file for the config map which contains the Caddyfile, and generates a set of random credentials for the deployment.

When an instance of the SchemaSpy image is started, it's Caddyfile is replaced with a copy of the one from the config map, and the basic authorization credentials are sourced from environment variables that are retrieving their values from secrets.