# TheOrgBook Database(s)

## Overview

TheOrgBook DB is used to store the core Organizational data for searching (notably names, locations/addresses and claims held) and the claims themselves.

## Development

The DB component is an instance of Postgres. The schema and data loading is all handled by TheOrgBook API, and the Postgres image being used is a Red Hat image. As such, there is no build or database initialization associated with the DB - just the Deployment.

# Database Schema Documentation

Databases are documented using [SchemaSpy](https://github.com/bcgov/SchemaSpy).