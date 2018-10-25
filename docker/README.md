# Running TheOrgBook with Docker Compose

The following instructions provide details on how to deploy the project using Docker Compose.  This method of deployment is intended for local development and demonstration purposes.  It is **NOT** intended to be support production level deployments where security, availability, resilience, and data integrity are important.

All application services are exposed to the host so they may be easily accessed individually for development and testing purposes.

## Prerequisites

* Docker and Docker Compose
  * Install and configure Docker and Docker compose for your system.
* The S2I CLI
  * Download and install the S2I CLI tool; [source-to-image](https://github.com/openshift/source-to-image)
  * Make sure it is available on your `PATH`.  The `manage` will look for the `s2i` executable on your `PATH`.  If it is not found you will get a message asking you to download and set it on your `PATH`.

## Management Script

The `manage` script wraps the Docker and S2I process in easy to use commands.

To get full usage information on the script run:

```sh
./manage
```
  
## Building the Images

The first thing you'll need to do is build the Docker images.  Since this requires a combination of Docker and S2I builds the process has been scripted inside `manage`.  _The `docker-compose.yml` file does not perform any of the builds._

To build the images run:
```sh
./manage build
```

## Starting the Project

To start the project run:

You will need to choose a unique seed value for development. Use a value that no one else is using. It must be 32 characters long exactly.


```sh
./manage start seed=my_unique_seed_00000000000000000
```

This will start the project interactively; with all of the logs being written to the command line.

Each seed must be authorized on the Indy ledger. If you are running the VON Network component locally, then DID registration is automatic. If using a shared Indy ledger then you will need to request authorization.


## Stopping the Project

To stop the project run:
```sh
./manage stop
```

This will shut down all of the containers in the project.

## Using the Application

* The main UI is exposed at; http://localhost:8080/
* The API is exposed at; http://localhost:8081/
* Schema-Spy is exposed at; http://localhost:8082/
* Solr is exposed at; http://localhost:8983/
* The database is exposed at; localhost:5432

## Loading Data

To load sample data into the running application use the `loadData.sh` script:
```sh
../openshift/loadData.sh -e http://localhost:8081
```

This will load sample data directly into the exposed REST API.

# Running a Complete Provisional VON Network

A "complete" provisional VON Network consists of the following components;
- A Provisional Ledger Node Pool; [von-network](https://github.com/bcgov/von-network)
- An instance of TheOrgBook; [TheOrgBook](https://github.com/bcgov/TheOrgBook)
- And a set of Issuer Services; [Permitify](https://github.com/bcgov/permitify)

The following **Quick Start Guide** will have you up and running in no time.  For specific details on the features and operation of the individual components refer to the docker compose documentation of the given projects.  For now, let's get you started with a working set of applications ...

## Quick Start Guide

1. Open shell windows (Git Bash for instance) to your working copies of `.../von-network`, `.../TheOrgBook/docker`, and `.../permitify/docker`.
1. In turn, run `./manage build` in each of the shell windows.
1. Wait for the builds to complete.
1. From `.../von-network` run `./manage start`, and wait for the von-network components to fully start.
1. Ensure the node pool is running by opening a browser window to http://localhost:9000
1. From `.../TheOrgBook/docker` run `./manage start seed=the_org_book_0000000000000000000`
1. Wait for the TheOrgBook's components to start up.
1. Ensure TheOrgBook is running by opening a browser window to http://localhost:8080/en/home
1. From `.../permitify/docker` run `./manage start`
1. Wait for all of the issuer services to start up.
1. Ensure the issuer services are running by opening a browser window to http://localhost:5000/ to start.  Each service starts up on a different port starting with 5000, the next on 5001, and so on.
1. You should now be able to browse to http://localhost:5000 and walk though the **Permitify Demo - Starting a Restaurant Recipe** demo, starting with registering an organization.

## Tips and Tricks

The component containers use persistent volumes, which can be a bit of an issue from time to time during testing as the various ledgers and wallets may get out of sync.  To clear out the volumes and start again you can use the following management command included in each of the projects.

```sh
./manage rm
```

This command will stop and remove any project related containers, and then remove their associated volumes.

### Live Web Development

TheOrgBook can also be brought up in a state where local modifications to the tob-web component are detected automatically, resulting in recompilation of the Javascript and CSS resources and a page reload when viewed in a web browser. To run TheOrgBook using this method execute:

```sh
./manage web-dev
```

# Current State

The project is fully wired together and functional.

None of the services define persistent storage.  If the images change and/or the containers from a previous run are removed, the data in the containers will be lost.

## Start-up Orchestration

The API server manages the database schema and indexes, therefore it must wait until the database and search engine (Solr) services are up and running AND fully initialized.  Likewise, the Schema-Spy service must wait until the API service has created/migrated the database schema to the most recent version before it starts.

To accomplish this the docker compose file defines simple sleep commands to pause the startup for these services.  It would be nice to develop a more deterministic solution for the start-up orchestration.  In the case of the API server it would sufficient to detect that Solr and PostgreSQL are responding, however, in the case of the Schema-Spy service this would be insufficient as the API server needs time to create or migrate the schema to the latest version before Schema-Spy starts.
