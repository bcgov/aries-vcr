# angular-scaffold

This project provides a baseline code base to help you kick start an Angular project that is based on BC Goverment themed Bootstrap styles, footers and headers.


This application has a complete development environment set up, including build, test, deploy, routing, simple components, service, and directives as examples and templates.

The goal is to help you start a project fast, enable you to focus on building actual business logics for your project.

[Check out a running demo of just scaffold out of the box](https://angular-scaffold-demo.pathfinder.gov.bc.ca)

# Development Prerequisites

## Node and NPM 

Node 6.9.x or greater must be installed (an angular-cli requirement).

## Install angular/cli

**Note, use `angular/cli`, do not use `angular/angular-cli`**

`npm i -g @angular/cli`

`ng` is the CLI itself 

    Verify the installation

    `npm list -g @angular/cli --depth=0`
    `ng -v`

### Install [yarn](https://yarnpkg.com/lang/en/docs/install/#alternatives-tab).

`npm i -g yarn`

## Fork, Build and Deployment

1. After installing Node and Yarn, you can fork or straight download a copy of this application to start your own app.
1. First download all the dependencies with `yarn install`
1. `npm start` to start the a webpack server to run the application on port 4300

    Go to http://localhost:4300 to verify that the application is running

    To change the default port, open `.angular-cli.json`, change the value on default.serve.port
1. Run `npm run build` to build the project. The build artifacts will be stored in the `dist/` directory. Use the `-prod` flag for a production build, like so: `ng serve --prod` to run in production mode.
1. `npm run lint` to check styles


## Code scaffolding

Run `ng generate component component-name` to generate a new component. You can also use `ng generate directive|pipe|service|class|module`.

### Example: Generate a customer component

`ng g c customer -d`

### Example: Generate a directive: search-bpx
`ng g d search-box -d`

### Example: Generate a service: general-data

`ng g s general-data -d`

Angular will give out a warning line after this command, `
WARNING Service is generated but not provided, it must be provided to be used
`
After generating a service, we must go to its owning module and add the service to the `providers` array.

### Example: Generate a service & include it in a module automatically

`ng g s general-data2 -m app.module`

### Example: Generate a class, an interface and emum

`ng g cl models/customer`

`ng g i models/person`

`ng g enum models/gender`

### Example: Generate a pipe

`ng g pipe shared/init-caps`

## Generate a module

Create a login directory and generate a login module in that directory

`ng g module login/login.module`

## Add/Generate Routing Features

Generate a module called admin and add routing feature to it.

`ng g module admin --routing`


## Accessibility Guidance

For guidance on how to make your app accessible, see our `/ACCESSIBILITY.md` docs for more info.

## Running Tests

### Unit tests
  
  Set up via Karma, Jasmin
1. `ng test` by default to watch file changes

### End-to-end tests
    Set up with Protractor
Run `ng e2e` to execute the end-to-end tests via [Protractor](http://www.protractortest.org/).
Before running the tests make sure you are serving the app via `ng serve`.


## Getting Help

1. To get more help on the Angular CLI use `ng help` or go check out the [Angular CLI README](https://github.com/angular/angular-cli/blob/master/README.md).
1. `ng doc component` to look up documentation for features
1. `ng serve --help` to look up doc for `ng serve` command


## Change aspects of the application

### Change style dialect

`ng set default.styleExt css`

## Regnerate a brand new project with routing and scss options

`ng new my-app --routing --style scss`

# Build and Deployment

For dev, test, and production builds on OpenShift/Jenkins see `openshift/README.md` for detailed instructions
on how to setup in an OpenShift environment using nginx.
