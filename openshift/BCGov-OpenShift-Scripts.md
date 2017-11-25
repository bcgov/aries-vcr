# BC Gov OpenShift Scripts

This project is using a series of scripts created to support BC Government projects deployed to the BC Government Pathfinder instance of OpenShift.  The following an initial, brief summary of the assumptions made in the scripts and the structure of, and conventions used in, this Project.

## projects

The scripts assume that the project will have a name (e.g. "devex-von") and four associated OpenShift projects - tools, dev, test and prod.

## Folder /openshift

The scripts are currently all found within the /openshift folder of the Project repositories. It is expected that if this approach gains traction in other projects, the scripts will be externalized from all projects and assumed to be accessible on the user's path.

In addition to the scripts (\*.sh) themselves, the /openshift folder contains:

* a *scripts* subfolder that houses some utility scripts
* a *settings.sh* file that contains a number of environment variables with presets for the Project
  * For a new project, this file must be updated with Project specific information
* an optional *settings.local.sh* file that can be used by a user to override Project settings for local deployment
* an optional number of other *\*.local.param* files that are used locally by a user to override Project settings (more on param files later)

**NOTE**: Files that contain "\*local\*" are gitignore'd by the Project and so are NOT pushed to the repository. Such files are purely for local use.

## Component Folders

Also in the root of the project are some number of folders containing "components" of the project. Loosely - a component is an element of the project that is (optionally) built and deployed - a database, a frontend JavaScript app, an API Server, etc. The *settings.sh* file in /openshift has a variable set to the list of components in the project.

## Build and Deploy Templates

The scripts expected to find within each component a */templates* folder, in and in that, some number of json files that are the build and deploy OpenShift templates.  By convention, the BuildConfig and DeploymentConfig templates MUST be separated.

* All Build templates will be used to create the BuildConfigs and ImageStreams (and support entities) in the Projects OpenShift "tools" project.
  * A Build Config template is assumed to be any JSON file within /templates that contains the string "BuildConfig"
* All Deployment templates are used to create Deployments in the dev, test and prod OpenShift projects.
  * A Deployment Config template is assumed to be any JSON file within /templates that contains the string "DeploymentConfig"

The json templates may be nested below the */templates* folder, but **they must be uniquely named**.

## JenkinsFiles

"JenkinsFile" found anywhere in the project are processed as Pipeline files and the Pipelines are created within the OpenShift "tools" project after the build templates are processed. In processing the JenkinsFiles, a deployment of Jenkins is deployed in the "tools" project.

## Param Files

In OpenShift, each json template may contain some number of parameters that are defaulted in the template and can be overridden on use. The scripts use a convention to support Project and local overrides of those parameters.

* For every Build or Deployment template, there is in the /<component> folder a *<template json name>.param* file that contains the list of the parameters for the template for the project. Those files should be edited and pushed to github.
* For every Deployment template, there is in the /<component> folder a *<template json name>.<env>.param* file that contains the list of parameters overrides for the template that are specific to that <env> (dev, test or prod). Most of the parameters are commented out, but some may vary by environment.
* For every Jenkinsfile, there is beside it a *pipeline.param* file that contains the list of pipeline template parameters and their values for that pipeline instance for the project.
  * There can also be a *pipeline.local.param* file containing user overrides for the parameters.

A script *genParams.sh* can be used to generate the parameter files - project, environment or local. See the usage (-h) on the script for how to use it.

## Basic Logic

The basic logic of the scripts are as follows. See the "Running Local" markdown file in the root of this project for a description of how to run the scripts:

* Generate Projects - a script that deletes or generates local instances of the OpenShift project - tools, dev, test, prod. This script will NOT run if you are connected to the Pathfinder instance of OpenShift.
* Initialize OS Projects - a script that does some necessary initialization of the OpenShift projects - settings permissions, adding persistence, etc.
* Generate Builds - process all of the Build JSON Templates, using any parameter files. In addition, process all of the Jenkins pipeline templates and parameter files.  If necessary, manually kick off any builds that don't autobuild, and then tag all of the promotable images with the "dev" tag.
  * Pauses are left in the script so that the user can fiddle within the OpenShift Web Console to get the build completed before the tagging process.
* Generate Deployments - process all of the Deployment JSON Templates, using any parameter files.
* If necessary, there is a script to update the routes of the deployments in the event that the templates hardcode the routes to Pathfinder.

## Current Status

The scripts are functional in the "devex-von" project only in this repo. Some work will be needed to fully externalize them - independent of any single project.

As noted above - the scripts expect the settings, file layouts and conventions described above to be in place. For use on any project, those conditions must be met.

The scripts do not account for extended pipelines incorporating additions like Sonarqube, post-build test steps, or promotion. They may work, but it depends on how those elements of the pipeline are manifest.
