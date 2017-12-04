# Running TheOrgBook Locally on OpenShift

These instructions assume:

* a moderate to advanced knowledge of OpenShift. There are two good PDFs available from Red Hat and O'Reilly on [OpenShift for Developers](https://www.openshift.com/promotions/for-developers.html) and [DevOps with OpenShift](https://www.openshift.com/promotions/devops-with-openshift.html) that should be read and understood first.
* you have forked and cloned [TheOrgBook repo](https://github.com/bcgov/TheOrgBook) and are accessing it on the command line.
* you are using a reasonable shell. A "reasonable shell" is obvious on Linux and Mac, and is assumed to be the git-bash shell on Windows. ~~PowerShell~~
* you have a Docker environment installed and running happily.

# Getting Started - oc cluster up

Get a recent stable (or the latest) [Openshift Command Line tool](https://github.com/openshift/origin/releases) (oc), install it and run ```oc cluster up``` to start OpenShift. Learn about how to run oc such that the configuration is preserved across machine reboots (e.g. ```oc cluster up --host-data-dir=//var/lib/origin/data --use-existing-config```). To install OC, you just need to download the release file, extract the "oc" executable and place it somewhere on your path.

**Login** to your local OpenShift instance on the command line and the Web Console.

# Change into the openshift folder at the root of TheOrgBook

```
cd openshift
```

# Create projects

If you are resetting your environment, change into the "openshift" folder in the root of TheOrgBook repo and run the following script.  Give this operation a bit of time to complete before recreating the projects.

```
./generateLocalProjects.sh -D
```

Run the following command to create the projects for the local instance. Test and Prod will not likely be used, but are referenced in some of the later scripts:

```
./generateLocalProjects.sh
```

# Initialize the projects - add permissions and storage

For all of the commands mentioned here, you can use the "-h" parameter for usage help and options.

```
./initOSProjects.sh
```

If you are running locally you will see some "No resources found." messages which can be ignored.

# Generate the Build and Images in the "tools" project; Deploy Jenkins

On the command line, change into the "openshift" folder in the root of TheOrgBook repo and run the script:

```
./genBuilds.sh -h
```

Review the command line parameters and pass in the appropriate parameters - without the -h.  For an initial install, no parameters are needed.

As of this writing, on some local OpenShift instances, builds fail because of resource limitations. Instructions are in the script to help with that scenario - things you have to do in the OpenShift Console. There are further instructions at the bottom of this Readme of how you can add local overrides that might prevent the hangs in the first place.

## Updating Build and Image Configurations

If you are adding build and image configurations you can re-run this script.  You will encounter errors for any of the resources that already exist, but you can safely ignore these areas and allow the script to continue.

If you are updating build and image configurations use the `-u` option.

If you are adding and updating build and image configurations, run the script **without** the `-u` option first to create the new resources and then again **with** the `-u` option to update the existing configurations.

# Generate the Deployment Configurations and Deploy the Components

On the command line, change into the "openshift" folder in the root of TheOrgBook repo and run the script:

```
./genDepls.sh -h
```

Review the command line parameters available and rerun with the appropriate parameters - without the -h. For an initial deploy, no parameters are needed.

As of this writing, on some local OpenShift instances, deployments fail because of resource limitations. Instructions are in the script to help with that scenario - things you have to do in the OpenShift Console. There are further instructions at the bottom of this Readme of how you can add local overrides that might prevent the hangs in the first place.

## Updating Deployment Configurations

If you are adding deployment configurations you can re-run this script.  You will encounter errors for any of the resources that already exist, but you can safely ignore these areas and allow the script to continue.

If you are updating deployment configurations use the `-u` option.

If you are adding and updating deployment configurations, run the script **without** the `-u` option first to create the new resources and then again **with** the `-u` option to update the existing configurations.

**_Note;_**

**_Some settings on some resources are immutable.  You will need to delete and recreate the associated resource(s).  Care must be taken with resources containing credentials or other auto-generated resources, however.  You must insure such resources are replaced using the same values._**

**_Updating the deployment configurations can affect (overwrite) auto-generated secretes such as the database username and password._**

# Fixing routes

In the current instance of the deployment, the routes created are explicitly defined for the Pathfinder (BC Gov) instance of OpenShift. Run the script to create the default routes for your local environment:

```
./updateRoutes.sh
```

# Loading Data

To load the test data into your instance of OpenShift, run:

```
./loadData.sh
```

You should see a series of blocks of data and "201" return code. If you see errors messages, the data step had "challenges". Contact us with questions.

If the load data step fails, you can:

- go to the APISpec/TestData folder in the repository
- view and run the "./load-all.sh" script. If you are loading data into the local environment, use an argument of "local"

NOTE: Data loads cannot be run multiple times. If you want to reload the data, you must first delete the database. You can do that by redeploying the entire environment, or going into Postgres and drop/recreating the database (instructions not yet available).

# Hangs, Corrections and Overrides

The generation of builds and deployments may hang because the environment on which you are running has fewer resources (especially less memory) than is requested in the templates. The scripts give you some guidance as to what you need to do to manually fix your current setup run. Notably:

* Cancel the current action (build or deploy)
* Remove the resources settings in either the YAML (build config) or be clearing the fields in the "Resource Limits" screen (deployment config).

The scripts also have a mechanism to override default parameters that should allow you to eliminate these hangs. The BuildConfig and DeploymentConfig overrides occur by setting values in template "param" files that override the defaults for the app. For local overrides, perform the steps below.

## Generate Local Param Files

Run the following script to generate a series of files with the extension ".local.param" in the "openshift" folder in the root of the repository:

```
./genParams -l
```

The files have all the parameters from the various templates in the project, with all of the parameters initially set to be commented out.

## Override the settings that cause the hangs

Find the .local.param file associated with the process that is hanging, edit that file, uncomment and change the parameter that is causing the hang.

NOTE: All *.local.* files are .gitignore'd and so will not be pushed into the repo.

For example, the ones that I find need overriding on my system are all related to builds or deploys that fail because of memory limitations. When the hang occurs, check the Web Console "Monitoring" and you will see a warning and message like: "No nodes are available that match all of the following predicates:: Insufficient memory (1)."

The fixes I applied are to the files:

* angular-on-nginx-build.local.param
* django-deploy.local.param
* schema-spy-deploy.local.param

In all case I need to uncomment and set this parameter:

MEMORY_LIMIT=0Mi
