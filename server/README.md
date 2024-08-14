# TheOrgBook API

## Overview

The API provides an interface into the database for The Credential Registry.

## Development

The API is developed in Django/Python.

## Debugging

### Visual Studio Code

`aries-vcr` is configured for debugging while running in its Docker environment using [Visual Studio Code](http://code.visualstudio.com).


## Database Migrations

Migrations are triggered automatically when the Django/Python container is deployed.  The process it triggered by wrapper code injected as part of the s2i-python-container build; https://github.com/sclorg/s2i-python-container/blob/master/3.6/s2i/bin/run
