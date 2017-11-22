# TheOrgBook API

## Overview

The API provides an interface into the database for TheOrgBook.

## Development

The API is developed in Django/Python, using a Visual Studio 2017 project.

## Development

To deploy TheOrgBook on an instance of OpenShift, see [the instructions](../RunningLocal.md) in the file RunningLocal.md.

## Development Deployment Environment

- [Schema Spy](http://schema-spy-devex-von-dev.pathfinder.gov.bc.ca/)
- [Open API (Swagger) API Explorer](http://django-devex-von-dev.pathfinder.gov.bc.ca/api/v1/)

## Database Migrations

Migrations are triggered automatically when the Django/Python container is deployed.  The process it triggered by wrapper code injected as part of the s2i-python-container build; https://github.com/sclorg/s2i-python-container/blob/master/3.6/s2i/bin/run

## ToDo:
- The auto-generated views are constructed using generics and a number of mixins.
  - Determine if there is a better way to do this.  Since it's not as clean as something constructed from ModelSerializer or HyperlinkedModelSerializer.
- Logging; ref gwells
