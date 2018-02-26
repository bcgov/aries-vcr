# TheOrgBook DB

## Overview

TheOrgBook DB is used to store the core Organizational data for searching (notably names, locations/addresses and claims held) and the claims themselves.

## Development

The DB component is an instance of Postgres. The schema and data loading is all handled by TheOrgBook API, and the Postgres image being used is an unchanged Red Hat image. As such, there is no build or database initialization associated with the DB - just the Deployment.

## Deployment

To deploy TheOrgBook on an instance of OpenShift, see [the instructions](../RunningLocal.md) in the file RunningLocal.md.

# Registries DB

## Overview

Internally TheOrgBook connects to an instance of the registries database (Oracle) via an a PostgreSQl database via oracle_fdw.

Refer to [Oracle-fdw-Testing](Oracle-fdw-Testing.md) for information on configuration and testing the connection.

# Database Schema Documentation

Databases are documented using [SchemaSpy](https://github.com/bcgov/SchemaSpy).  The documentation of the Oracle database requires Oracle JDBC drivers.  Due to licensing restrictions the image for the associated pod has been built manually and pushed into the project's tools project.