# Running TheOrgBook Locally on OpenShift

These instructions assume:

* a moderate to advanced knowledge of OpenShift. There are two good PDFs available from Red Hat and O'Reilly on OpenShift for Developers and OpenShift DevOps that should be read and understood first.
* you have forked and cloned [TheOrgBook repo](https://github.com/bcgov/TheOrgBook) and are accessing it on the command line.
* you are using a reasonable shell. A "reasonable shell" is obvious on Linux and Mac, and is assumed to be the git-bash shell on Windows. ~~PowerShell~~
* you have a Docker environment installed and running happily.

# Getting Started - oc cluster up

Get a recent stable (or the latest) [Openshift Command Line tool](https://github.com/openshift/origin/releases) (oc), install it and run ```oc cluster up``` to start OpenShift. Learn about how to run oc such that the configuration is preserved across machine reboots (e.g. ```oc cluster up --host-data-dir=//var/lib/origin/data --use-existing-config```).

Login to your local OpenShift instance on the command line and the Web Console.

# Create projects

Run the following commands to create the projects for the local instance. Test and Prod will not likely be used, but are referenced in some of the later scripts:

```
oc new-project devex-von-tools;
oc new-project devex-von-dev;
oc new-project devex-von-test;
oc new-project devex-von-prod;
```

# Initialize the Projects

On the command line, change into the "openshift" folder in the root of TheOrgBook repo and run the script:

```
MSYS_NO_PATHCONV=1 ./initializeProjects.sh devex-von
```

This will add some permissions necessary for deployment of the application and add some not-needed-for-local Glusterfs Services. Errors ("No resources found.") on the Glusterfs Service creation steps can be ignored.

# Deploy the database

On the command line, go into the folder "tob-db/openshift" and follow the instructions in the [Readme file](https://github.com/bcgov/TheOrgBook/tree/master/tob-db) in the parent folder.

# !!DANGER!! Watch out for "Insufficient Memory" Build Hangs

**NOTE**: On build the API and the Web components, it's possible that one or more of the build jobs could hang because of a lack of local resources (an Event "No nodes are available that match all of the following predicates:: Insufficient memory (1)."). If that happens:

* Cancel any Pending builds
* Go into the Build Config of the failing job via the Web Console
* Edit the YAML for the Build Config and remove the "Resources" section of the YAML file.

# Deploy the API

On the command line, go into the folder "tob-api/openshift" and follow the instructions in the [Readme file](https://github.com/bcgov/TheOrgBook/tree/master/tob-api) in the parent folder.

The API should now be deployed, but the route (URL) to the API is pointed at the BC Gov dev instance of TheOrgBook. To point it to the local instance, run the following commands:

```
oc delete route django;
oc create route edge --service django django;
oc delete route schema-spy;
oc create route edge --service schema-spy schema-spy;
```

This will create new routes to the local instance of the API and Schema Spy using the default naming convention - likely (for the API): https://django-devex-von-dev.10.0.75.2.nip.io.

Verify the API is running by hitting it's route URL.  You should see the Swagger UI running, and you should be able to execute a Swagger endpoint (e.g. GET inactiveclaimreasons) successfully, but get an empty dataset back (e.g. "[]").

# Load the Test data

On the command line, go into the "APISpec/Testdata" folder and run  following command. Note, if the route to your API is different than the expected one (listed above for the API), then change "local" to the URL:

```
MSYS_NO_PATHCONV=1 ./load-all.sh local
```

This should load test data into the database. Repeating the Swagger execution (e.g. GET inactiveclaimreasons) should now return some data.

**NOTE**: You should only run the "load-all" script once, or you get duplicates in your data. If you need to reload test data, you need to drop the database, recreate it and then load the data again.

# Deploy the Web Component

On the command line, go into the folder "tob-web/openshift" and follow the instructions in the [Readme file](https://github.com/bcgov/TheOrgBook/tree/master/tob-web) in the parent folder.

At this point, the Web Component should be deployed, but the route to the instance is going to the BC Gov dev instance of TheOrgBook. To point it to the local instance, run the following commands:

```
oc delete route angular-on-nginx;
oc create route edge --service angular-on-nginx angular-on-nginx;
```

This will create new routes to the local instance of the Web using the default naming convention - likely for the API: http://angular-on-nginx-devex-von-dev.10.0.75.2.nip.io.

Verify the API is running by hitting it's route URL.

**Note:** Currently, the Web instance is hard-coded to connect back to the BC Gov Dev instance of TheOrgBook.  While that is helpful for frontend development (no need to have a local instance of the API/DB), that's not the goal of running the app locally on OpenShift. We'll figure out how to fix that Real Soon Now. It appears there is an environment variable TOB_API_URL in the deployment config of "angular-on-nginx" that should control the API being used. However, changing it to use the local URL does not seem to work.
