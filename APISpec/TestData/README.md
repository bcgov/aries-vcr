TheOrgBook - Generating/Loading Test Data
======================

Overview
--------
This folder contains reference and test data for the TheOrgBook (TOB) application and a mechanism for managing and generating the reference and test data files. Reference data is read-only data that is loaded into all instances of the application (Dev, Test and Prod) - status values, type lists, etc. Test data is fake data in the correct format to be loaded into the Dev and/or Test instances of the application for use in testing the system. Note that some tables - such as the Fuel Supplier data might be both - used for testing on Dev and Test and used as the seed data going into production.

Managing/Creating the Data
---------------------
The data is maintained in the _TOBData.xlsm_ Excel file in the "in" folder. It has a series of tabs in it, and each one with a ".csv" extension is exported from the excel and used to drive the data generation process.  The test data itself is a combination of static data and formulas to generate data (e.g. random dates, values, etc.) and joins between tables. There is also a table of fake names and addresses to use for people/users in the system.

A VB Excel macro, invoked with the key combination Ctrl-Shift-V, exports all of the csv files in one step. Use the macro every time you update the test data.

Once exported, use the "gendata.bat" or "gendata.sh" scripts to generate the JSON files that make up the test data. The JSON files are (or should be) compatible with the "bulk" operations generated from the Swagger API. Loaded in the correct order, they will initialize the data to a proper state.

Loading the Test Data
----------------
Once the data is generated, scripts are used to load the data via the API.

The `load.sh` script takes as arguments:

* a JSON file
* an "bulk" API endpoint
* a server URL (literal dev, test or prod or a full URL)

and loads the data into the application using the given endpoint.  The `load.sh` script includes a commented out call to authenticate the user with the application and create a cookie for the subsequent call to actually load the data. The authenticate call is expected to only be called if the "cookie" file does not exist.

The `load-all.sh` script takes just the server as an argument (same format as `load.sh` to be loaded and loads in relational appropriate order all of the tables to initialize the application.  The load-all script removes the "cookie" file if it exists so that on only the first call to the load script, the (currently commented out) authentication call will be made to the server.

The Process
----------------
The following is a simplified version of a more detailed process documented here; [Detailed Steps to reset the Database for an environment](https://github.com/bcgov/hets/tree/master/APISpec/TestData#detailed-steps-to-reset-the-database-for-an-environment).  The idea is to _eventually_ completely automate the process.

These instructions assme you are using the OpenShift managment scripts found here; [openshift-project-tools](https://github.com/BCDevOps/openshift-project-tools).  Refer to the [OpenShift Scripts](https://github.com/BCDevOps/openshift-project-tools/blob/master/bin/README.md) documentation for details.

1. Open a Git Bash command prompt to your project's root `openshift` directory.
1. Switch to the appropriate OpenShift project.
   - `oc project devex-von-dev`
1. Scale the API server (django) to zero pods, and wait for the deployment to be scaled to zero (monitor the progress in the OpenShift console);
   - `scaleDeployment.sh django 0`
1. Recreate the database (postgresql);
   - `dropAndRecreateDatabase.sh devex-von-dev postgresql TheOrgBook_Database TheOrgBook_User`
1. Scale the API server (django) back up to it's working set of pods, and wait for the deployment to be scaled back up (monitor the progress in the OpenShift console).  The database schema will get created as part of the migration process as the pods(s) come up.
   - `scaleDeployment.sh django 1`
1. Use the `loadData.sh` script to populate the database through the API server.
   - `loadData.sh -e dev`
1. Rebuild the Solr search index;
   - `runInContainer.sh django 'python ./manage.py rebuild_index --noinput'`

ToDo:
- Wrap the above in a master script that has the user wait between the steps.