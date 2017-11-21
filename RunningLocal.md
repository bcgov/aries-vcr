# Running TheOrgBook Locally on OpenShift

These instructions assume:

* a moderate to advanced knowledge of OpenShift. There are two good PDFs available from Red Hat and O'Reilly on [OpenShift for Developers](https://www.openshift.com/promotions/for-developers.html) and [DevOps with OpenShift](https://www.openshift.com/promotions/devops-with-openshift.html) that should be read and understood first.
* you have forked and cloned [TheOrgBook repo](https://github.com/bcgov/TheOrgBook) and are accessing it on the command line.
* you are using a reasonable shell. A "reasonable shell" is obvious on Linux and Mac, and is assumed to be the git-bash shell on Windows. ~~PowerShell~~
* you have a Docker environment installed and running happily.

# Getting Started - oc cluster up

Get a recent stable (or the latest) [Openshift Command Line tool](https://github.com/openshift/origin/releases) (oc), install it and run ```oc cluster up``` to start OpenShift. Learn about how to run oc such that the configuration is preserved across machine reboots (e.g. ```oc cluster up --host-data-dir=//var/lib/origin/data --use-existing-config```). To install OC, you just need to download the release file, extract the "oc" executable and place it somewhere on your path.

**Login** to your local OpenShift instance on the command line and the Web Console.

# Create projects

If you are resetting your environment, here is a list of commands to copy/paste to remove the project set. Give this operation a bit of time to complete before recreating the projects.

```
oc delete project devex-von-tools;
oc delete project devex-von-dev;
oc delete project devex-von-test;
oc delete project devex-von-prod;
```

Run the following commands to create the projects for the local instance. Test and Prod will not likely be used, but are referenced in some of the later scripts:

```
oc new-project devex-von-tools;
oc new-project devex-von-dev;
oc new-project devex-von-test;
oc new-project devex-von-prod;
```

# Change into the openshift folder at the root of TheOrgBook

```
cd openshift
```

# Initialize the projects - add permissions and storage

For all of the commands mentioned here, you can use the "-h" parameter for usage help and options.

```
./initOSProjects.sh
```

# Generate the Build and Images in the "tools" project; Deploy Jenkins

On the command line, change into the "openshift" folder in the root of TheOrgBook repo and run the script:

```
./genBuilds.sh -h
```

There are currently many "Hit a key to continue..." pauses in the script so that you can look at the Web Console to see what has changed after each step. For the Build - look at the Builds in the "devex-von-tools" project, for the deploy look at the Deployments in the "devex-von-dev" project.

Review the command line parameters and pass in the appropriate parameters - without the -h.  For an initial install, no parameters are needed.

As of this writing, on some local OpenShift instances, builds fail because of resource limitations. Instructions are in the script to help with that scenario - things you have to do in the OpenShift Console.

# Generate the Deployment Configurations and Deploy the Components

On the command line, change into the "openshift" folder in the root of TheOrgBook repo and run the script:

```
./genDepls.sh -h
```

Review the command line parameters available and rerun with the appropriate parameters - without the -h. For an initial deploy, no parameters are needed.

As of this writing, on some local OpenShift instances, deployments fail because of resource limitations. Instructions are in the script to help with that scenario - things you have to do in the OpenShift Console.

# Fixing routes

In the current instance of the deployment, the routes created are explicitly defined for the Pathfinder (BC Gov) instance of OpenShift. Run the script to create the default routes for your local environment:

```
./updateRoutes.sh
```

# Loading Data

To load the test data into your instance of OpenShift, run:

```
./loadData.sh -g
```

You should see a series of blocks of data and "201" return code. If you see errors messages, the data step had "challenges". Contact us with questions.

If the load data step fails, you can:

- go to the APISpec/TestData folder in the repository
- view and run the "./load-all.sh" script. If you are loading data into the local environment, use an argument of "local"

NOTE: Data loads cannot be run multiple times. If you want to reload the data, you must first delete the database. You can do that by redeploying the entire environment, or going into Postgres and drop/recreating the database (instructions not yet available).
