# TheOrgBook API

## Overview

The API provides an interface into the database for The Credential Registry.

## Development

The API is developed in Django/Python.

## Debugging

### Visual Studio Code

`aries-vcr` is configured for debugging while running in its Docker environment using [Visual Studio Code](http://code.visualstudio.com).

To run in debug mode, append DJANGO_DEBUG=True to your run command. For example, `./manage start DJANGO_DEBUG=True`. This will start the debugger software and wait for a remote debugger to be attached before proceeding further.

To add a new debugger session, create a `launch.json` file and add the following configuration:
```
{
    "name": "vcr-server",
    "type": "python",
    "request": "attach",
    "pathMappings": [
        {
            "localRoot": "${workspaceFolder}/server",
            "remoteRoot": "/home/indy"
        }
    ],
    "port": 3000,
    "host": "localhost"
}
```

## Database Migrations

Migrations are triggered automatically when the Django/Python container is deployed.  The process it triggered by wrapper code injected as part of the s2i-python-container build; https://github.com/sclorg/s2i-python-container/blob/master/3.6/s2i/bin/run
