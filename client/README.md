# TheOrgBook Web

## Overview

The Web implements the user interface for TheOrgBook, calling the API to manage data. The interface is served from an instance of [NGINX](https://www.nginx.com/).

## Development

Developing with data requires an instance of the Agent Issuer Controller or a connection to the test instance of BCovrign.

### Themes

Themes can be customized as per the [guide](ThemeDevelopment.md).

### Docker

A docker instance that runs hot-reloading can be initialized by following the steps located in the [developer guide](../../../docs/README.MD).

### Ng Serve

It is possible (but not recommended) to run the Web UI only in the development mode. To do this run the following command in the *vcr-web* directory.

When running for the first time, install the required node.js packages:

``` 
npm install
``` 

and

``` 
ng serve
```

