# Running TheOrgBook with Docker Compose

The following instructions provide details on how to deploy the project using Docker Compose.  This method of deployment is intended for local development and demonstration purposes.  It is **NOT** intended to be support production level deployments where security, availability, resilience, and data integrity are important.

All application services are exposed to the host so they may be easily accessed individually for development and testing purposes.

## Prerequisites

* Docker and Docker Compose
  * Install and configure Docker and Docker compose for your system.
* The S2I CLI
  * Download and install the S2I CLI tool; [source-to-image](https://github.com/openshift/source-to-image)
  * Make sure it is avaialble on your `PATH`.  The `manage.sh` will look for the `s2i` executable on your `PATH`.  If it is not found you will get a message asking you to download and set it on your `PATH`.

## Management Script

The `manage.sh` script wraps the Docker and S2I process in easy to use commands.

To get full usage information on the script run:
```
./manage.sh -h
```
  
## Building the Images

The first thing you'll need to do is build the Docker images.  Since this requires a combination of Docker and S2I builds the process has been scripted inside `manage.sh`.  _The `docker-compose.yml` file does not perform any of the builds._

To build the images run:
```
./manage.sh build
```

### Troubleshooting the Building

If you get errors during the build that reference scripts such as the following, check the line endings of your local copy of the file.  Replace `CRLF` line endings with `LF` and rebuild the image.

The `.gitattributes` file for the project has been updated, but if your local copy predates the update, your files may still be affected.

```
/bin/sh: 1: /usr/libexec/s2i/assemble-runtime: not found
error: Execution of post execute step failed
Build failed
ERROR: An error occurred: non-zero (13) exit code from angular-builder
```

In this example search your working copy for all instances of `assemble-runtime`.

## Starting the Project

To start the project run:

You will need to choose a unique seed value for development. Use a value that no one else is using. It must be 32 characters long exactly.


```
./manage.sh start seed=my_unique_seed_00000000000000000
```

This will start the project interactively; with all of the logs being written to the command line.

Each seed, must be authorized on the indy ledger. If you are using the https://github.com/bcgov/von-network network locally, you can visit the webserver running on your local machine to authorize the did for each seed. If you are using the shared development Indy ledger (which is an instance of von-network), you can visit this page to authorize your did: http://138.197.170.136


## Stopping the Project

To stop the project run:
```
./manage.sh stop
```

This will shutdown all of the containers in the project.

## Using the Application

* The main UI is exposed at; http://localhost:8080/
* The API is exposed at; http://localhost:8081/
* Schema-Spy is exposed at; http://localhost:8082/
* Solr is exposed at; http://localhost:8983/
* The database is exposed at; localhost:5432

## Loading Data

To load sample data into the running application use the `loadData.sh` script:
```
../openshift/loadData.sh -e http://localhost:8081
```

This will load sample data directly into the exposed REST API.

# Current State

The project is fully wired together and functional.

None of the services define persistent storage.  If the images change and/or the containers from a previous run are removed, the data in the containers will be lost.

## Start-up Orchestration

The API server manages the database schema and indexes, therefore it must wait until the database and search engine (Solr) services are up and running AND fully initialized.  Likewise, the Schema-Spy service must wait until the API service has created/migrated the database schema to the most recent version before it starts.

To accomplish this the docker compose file defines simple sleep commands to pause the startup for these services.  It would be nice to develop a more deterministic solution for the start-up orchestration.  In the case of the API server it would sufficient to detect that Solr and PostgreSQL are responding, however, in the case of the Schema-Spy service this would be insufficient as the API server needs time to create or migrate the schema to the latest version before Schema-Spy starts.
