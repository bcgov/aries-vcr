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

It is assumed you have an instance of Permitify running to run this script, and you have working copies of both the Permitify and TheOrgBook source code.

1. Open 2 Git Bash command prompt windows; one to your `.../permitify/openshift` working directory and the other to your `.../TheOrgBook/openshift` working directory.
1. From the `.../TheOrgBook/openshift` command prompt, run the manage command to reset the database in TheOrgBook environment.
    - For example; 
        - `./manage -P -e dev resetDatabase`
    - For full usage information run;
        - `./manage -h`
1. From the `.../permitify/openshift` command prompt, run the manage commands to recycle all of the Permitify service pods.  This is needed because issuers must register themselves with TheOrgBook before they can issue claims.
    - For example; 
        - `./manage -e dev recycle`
    - For full usage information run;
        - `./manage -h`
1. Wait for all of the Permitify services to full start before continuing.
1. Use the `load-all.sh` script to populate the database through the Permitify services.
   - `./loadData.sh {local|dev|test}`