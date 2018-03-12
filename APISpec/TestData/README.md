TheOrgBook - Generating/Loading Test Data
======================

Overview
--------
This folder contains reference and test data for the TheOrgBook (TOB) application and a mechanism for managing and generating the reference and test data files. The load script uses an instance of Permitify to create and send claims as multiple systems are required to generate verifiable claims.

Managing/Creating the Data
---------------------
The data is maintained in the Claims directory as a series of "recipes". Each JSON file can be used to automate data entry for an entire TOB recipe workflow.

TODO: describe method to generate data

Loading the Test Data
----------------
Once the data is generated, scripts are used to load the data via the Permitify services.

The `load-all.sh` script takes just the server as an argument (same format as `load.sh` to be loaded and loads in relational appropriate order all of the tables to initialize the application.  The load-all script removes the "cookie" file if it exists so that on only the first call to the load script, the (currently commented out) authentication call will be made to the server.

The Process
----------------

These instructions assume you are using the OpenShift management scripts found here; [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools).  Refer to the [OpenShift Scripts](https://github.com/BCDevOps/openshift-project-tools/blob/master/bin/README.md) documentation for details.

It is assumed you have an instance of Permitify running to run this script.

1. Open a Git Bash command prompt to your project's root `openshift` directory.
1. Switch to the appropriate OpenShift project.
   - `oc project devex-von-dev`
1. Scale the API server (django) to zero pods, and wait for the deployment to be scaled to zero (monitor the progress in the OpenShift console);
   - `scaleDeployment.sh django 0`
1. Recreate the database (postgresql);
   - `dropAndRecreateDatabase.sh devex-von-dev postgresql TheOrgBook_Database TheOrgBook_User`
1. Scale the API server (django) back up to it's working set of pods, and wait for the deployment to be scaled back up (monitor the progress in the OpenShift console).  The database schema will get created as part of the migration process as the pods(s) come up.
   - `scaleDeployment.sh django 1`
1. Reboot all of the Permitify pods. This is needed because issuers must register themselves with TheOrgBook before they can issue claims.
    - `oc project devex-von-permitify-dev`
    - `scaleDeployment.sh worksafe-bc 0`
    - `scaleDeployment.sh ministry-of-finance 0`
    - `scaleDeployment.sh liquor-control-and-licensing-branch 0`
    - `scaleDeployment.sh fraser-valley-health-authority 0`
    - `scaleDeployment.sh city-of-surrey 0`
    - `scaleDeployment.sh bc-registries 0`
    - Wait for all of the pods to scale down completely...
    - `scaleDeployment.sh worksafe-bc 1`
    - `scaleDeployment.sh ministry-of-finance 1`
    - `scaleDeployment.sh liquor-control-and-licensing-branch 1`
    - `scaleDeployment.sh fraser-valley-health-authority 1`
    - `scaleDeployment.sh city-of-surrey 1`
    - `scaleDeployment.sh bc-registries 1`
    - `oc project devex-von-dev`
1. Use the `load-all.sh` script to populate the database through the Permitify services. (Assumes permitify is running)
   - `./loadData.sh --env {local|dev|test}`
1. Rebuild the Solr search index;
   - `runInContainer.sh django 'python ./manage.py rebuild_index --noinput'`

ToDo:
- Wrap the above in a master script that has the user wait between the steps.

Creating/Loading Test Data
--------------------
The load-all.sh can be used to create test data, using the following optional parameters:

```
$./load-all.sh -h
Data for TheOrgBook is now loading via the loading of claims. Details to come...
usage: loadClaims.py [-h] [--random] [--env env] [--inputdir inputdir]
                     [--threads threads] [--loops loops]

A TheOrgBook Claim loader. Supports randomization for test data and threading
for fast loading

optional arguments:
  -h, --help           show this help message and exit
  --random             If data is to be randomized before loading (useful for
                       test data)
  --env env            Permitify and TheOrgBook services are on local/dev/test
                       host
  --inputdir inputdir  The directory containing JSON claims to be loaded
  --threads threads    The number of threads to run for concurrent loading
  --loops loops        The number of times to loop through the list
```

The loader will load data from the data files as described above, however it can optionally "randomize" the data to support loading multiple copies, using the "--random" flag:

```
$./load-all.sh --random
```

You can spin up multiple threads, and loop through the input data multiple times, as follows:

```
$./load-all.sh --threads 4 --loops 10
```

When you specify either of these flags, then "--random" is enabled automatically.

There is also the option to load data directly into a wallet - this can be used for adding wallet data "through the back door" for performance testing.  This data won't have all the fancy anoncreds and can't be processed by the indy-sdk:

```
$./load-all.sh --env wallet
```
