# Running TheOrgBook with Docker Compose

## Prerequisites

* Docker and Docker Compose
  * Install and configure Docker and Docker compose for your system.
* The S2I CLI
  * Download and install the S2I CLI tool; [source-to-image](https://github.com/openshift/source-to-image)
  * Set a S2I_HOME env variable to point at the folder containing the s2i.exe tool.

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

## Starting the Project

To start the project run:
```
./manage.sh start
```

This will start the project interactively; with all of the logs being written to the command line.

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

To load sample data into the running applicaiton use the `loadData.sh` script:
```
../openshift/loadData.sh -e http://localhost:8081
```

This will load sample data directly into the exposed REST API.

# Current State

The application of operational, but not fully wired together and functional.  The current state is suitable as a PCO docker compose instance and for basic demos.

* All of the builds work.
* The main UI and the API are wired together and communicating.
* The API server is using a local SqlLite database and the direct to database search engine.

* Schema-Spy and Solr connecting to the database and are not functional yet.

* The database comes up, but dependent services do not wait for it to become ready.

## ToDo

* Configure database dependent service(s) to:
  * Wait for the database to become ready
  * Connect to the database
