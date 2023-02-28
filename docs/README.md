
# Hyperledger Aries VCR <!-- omit in toc -->

# Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Before You Start](#before-you-start)
- [Repositories](#before-you-start)
- [Prerequisites](#prerequisites)
- [Running a VON - Verified Organizations Network](#running-a-von---verified-organizations-network)
  - [Running on Docker Locally](#running-the-network-on-docker-locally)
  - [Stopping the Network](#stopping-the-network)
- [Aries VCR](#aries-vcr)
  - [Building the Images](#building-the-images)
  - [Starting the Project](#starting-the-project)
  - [Stopping the Project](#stopping-the-project)
  - [Using the Application](#using-the-application)
  - [Start-up Orchestration](#start--up-orchestration)
- [Aries VCR Issuer Controller](#aries-vcr-issuer-controller)
  - [Initialize the Project](#initialize-the-project)
  - [Register the DID](#register-the-did)
  - [Build and Start the Project](#build-and-start-the-project)
  - [Updates to Credential Schema](#updates-to-credential-schema)
  - [Issuing Credentials](#issuing-credentials)
- [Aries VCR Client](#aries-vcr-client)
- [Troubleshooting Guides](#troubleshooting-guides)

## Introduction

This guide is intended for use by teams and entities who are planning to or are currently working with the Aries VCR software components.

If you are unfamiliar with the underpinning technologies and concepts that are utilized in this project, you can review the [BC Government initiatives](https://digital.gov.bc.ca/digital-trust/) and [tools](https://digital.gov.bc.ca/digital-trust/tools/tools-overview/), and you can also ask questions in the [Hyperledger community discord channel](https://discord.com/servers/hyperledger-foundation-905194001349627914).

## Before you Start

Running this project in development requires a running VON - Verified Organizations Network, the Aries VCR project and an Aries VCR Issuer Controller.

Aries VCR is a cloud-based project that is developed as a cloud-native application. All components are developed in Docker first. _As such we __strongly recommend__ that using Docker for all development local or otherwise_.

_Note: The Aries VCR contributors do not test or develop any of the technical components on bare metal._

## Repositories

Running all components of an Aries VCR network in development requires the following repositories:

- [VON - Verified Organizations Network](https://github.com/bcgov/von-network)
- [Aries VCR](https://github.com/bcgov/aries-vcr)
- [Aries VCR Issuer Controller](https://github.com/bcgov/aries-vcr-issuer-controller)
- [Aries VCR Client](https://github.com/bcgov/aries-vcr-client)

It is recommended to fork all the listed repositories, **with the exception of the Issuer Controller**. If your use case requires an Issuer Controller follow the outlined procedure in the issuer-controller guide.

_Note: The Issuer Controller may not be necessary for your project implementation if there is no need for issuing credentials. It will still be required for development (to issue credentials) if you do not have a separate agent that you are using for issuing._

 _Note: The Client is also optional, but recommended if you are just starting out and/or want a ready-made user-interface for your credential registry._

## Prerequisites

- Docker and Docker Compose
  - Install and configure Docker and Docker compose for your system.

- [The S2I CLI](https://github.com/openshift/source-to-image/releases).
  - Download and install the S2I CLI tool; source-to-image
  - Running the S2I CLI tool with the manage script requires having the executable on your PATH. If it is not found you will get a message asking you to download and set it on your PATH.
- Manage Script
  - The manage script wraps the Docker and S2I process in easy to use commands.

## Running a VON - Verified Organizations Network

The following instructions provide details on how to deploy the project using Docker Compose. This method of deployment is intended for local development and demonstration purposes. It is NOT intended to support production-level deployments where security, availability, resilience, and data integrity are important.

### Running the Network On Docker Locally

Open a terminal session, change directories to where you store repos, and clone the von-network repository:
```bash
git clone <repository url> von-network
# Move to the new directory:
cd von-network
# Build the docker images that will be used to run the Indy network containers (this process will take several minutes):
./manage build
```

The `./manage` script has a number of commands. Run it without arguments to see the set of options.

Once the build process completes, you can test the build to make sure everything works properly:
```bash
./manage start --logs
```
Monitor the logs for error messages as the nodes start up.

Verify the network is running
In a browser, go to http://localhost:9000. You should see the VON Indy Ledger Browser and the status of the four nodes of the Indy Network. All should show a lovely, complete blue circle. If not - check the logs in the terminal.

### Stopping the Network

To stop the scrolling logs and get to a command prompt, hit `Ctrl-C`. To stop and remove the network persistence (the Ledger), run: 
```bash
./manage down
```
If necessary, you can use `./manage stop` instead of down to stop the containers but retain the persistence.

## Aries VCR

Fork the Aries VCR project as per the initial instructions at the outset.

Fork the project, navigate to the folder where you keep your projects and repositories and run:
```bash
git clone https://github.com/<username>/aries-vcr
```

Finally, change directory to the new created starter-kit located in the aries-vcr project folder:
```bash
cd aries-vcr/starter-kits/credential-registry/docker
```

### Building the Images

Building the images requires a combination of Docker and S2I builds. The process has been scripted inside manage. 

To build the images run: 
```bash
./manage build
```

### Starting the Project

The Aries VCR starter kit requires a unique seed for development. This is a 32 character value that uniquely identifies your wallet/ledger seed to the VON ledger running locally or on another network.

You can choose a unique seed value for development. Use a value that is not used by another agent within the environment. It must be 32 characters long exactly. If you're using an externally hosted VON ledger you will need to be careful to select a unique seed in this step.

Register the unique seed by running the following script command: 
```bash
./manage registerDids seed=my_unique_seed_00000000000000000
```

Finally run the manage script to start the project: 

```bash
./manage start seed=my_unique_seed_00000000000000000 --logs
```

Note that you can let the script choose a seed for you as follows:

```bash
./manage start --logs
```

This will start the project interactively; with all of the logs being written to the command line.

### Stopping the Project

There are two commands to stop the project. `Down` and `Stop`.

#### Stop

`Stop` stops the containers, but leaves the rest of the docker-compose structure in place - volumes (and the Indy wallets they store) and networking.

To stop the containers without destroying them run:
```bash
./manage stop
```

#### Down

`Down` is destructive, removing the volumes and network elements. Often in a debugging session, stop is sufficient. If you use down, you likely will have to restart the prerequisite Indy network.

To remove the volumes and network elements run: 
```bash
./manage down
```

### Building the "BC Gov" Version of the Images

You can build the BC Government specific version of the application as follows:

To build the images run: 

```bash
THEME=bcgov DEBUG=false ./manage build
```

... and then to run the application:

```bash
THEME=bcgov DEBUG=false ./manage start --logs
```

### Using the Application

- The API is exposed at: http://localhost:8081/
- Schema-Spy is exposed at: http://localhost:8082/
- Solr is exposed at: http://localhost:8983/
- The database is exposed at: http://localhost:5432/

### Start-up Orchestration

The API server manages the database schema and indexes, therefore it must wait until the database and search engine (Solr) services are up and running AND fully initialized. Likewise, the Schema-Spy service must wait until the API service has created/migrated the database schema to the most recent version before it starts.

To accomplish this, the docker compose file defines simple sleep commands to pause the startup for these services. It would be nice to develop a more deterministic solution for the start-up orchestration. In the case of the API server it would sufficient to detect that Solr and PostgreSQL are responding, however, in the case of the Schema-Spy service this would be insufficient as the API server needs time to create or migrate the schema to the latest version before Schema-Spy starts.

## Aries VCR Issuer Controller

There is an issuer-verifier agent that is available for use with your project. This is the [Aries VCR Issuer Controller](https://github.com/bcgov/aries-vcr-issuer-controller).

The tutorial for running this issuer is located [here](https://github.com/bcgov/aries-vcr-issuer-controller/blob/main/GettingStartedTutorial.md).

Note that if you are running the demo issuer with the "base" version of the Aries VCR API (as opposed to the BC Government version) you may see some errors when posting the credentials.  This is a known issue.  The posted credentials should still be visible through the Aries VCR Client and API.

## Aries VCR Client

The Client is an optional web application that provides a UI to the API for searching and viewing credential details. If you are a first-time user of Aries VCR, it is recommended to run the Client to see how the API can be consumed in a client-facing application. You may additionally choose to base your own registry client off of the Client (by extending the Client) or build your own from scratch.

See details in the [bcgov/aries-vcr-client](https://github.com/bcgov/aries-vcr-client) repo for more details on how to run and extend the Client where necessary. The Client can be simply run with the following command:

```bash
./manage build
./manage start --logs
```

Here are some examples of applications that have extended the base Client for their own purposes:

* [Orgbook BC](https://github.com/bcgov/orgbook-bc-client)
* [Orgbook ON](https://github.com/bcgov/orgbook-on-client)

## Troubleshooting Guides:
- [Fixing a Corrupt Wallet Index](./fix-corrupt-wallet-index.md)