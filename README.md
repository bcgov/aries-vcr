[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](LICENSE)

[![Bugs](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/api/badges/measure?key=TheOrgBook&metric=bugs&template=FLAT)](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/dashboard?id=TheOrgBook) [![Vulnerabilities](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/api/badges/measure?key=TheOrgBook&metric=vulnerabilities&template=FLAT)](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/dashboard?id=TheOrgBook) [![Code smells](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/api/badges/measure?key=TheOrgBook&metric=code_smells&template=FLAT)](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/dashboard?id=TheOrgBook) [![Coverage](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/api/badges/measure?key=TheOrgBook&metric=coverage&template=FLAT)](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/dashboard?id=TheOrgBook) [![Duplication](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/api/badges/measure?key=TheOrgBook&metric=duplicated_lines_density&template=FLAT)](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/dashboard?id=TheOrgBook) [![Lines of code](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/api/badges/measure?key=TheOrgBook&metric=lines&template=FLAT)](https://sonarqube-devex-von-tools.pathfinder.gov.bc.ca/dashboard?id=TheOrgBook) 

# TheOrgBook
# Hyperledger Indy Catalyst <!-- omit in toc -->

![logo](/docs/assets/indy-catalyst-logo-bw.png)

# Table of Contents <!-- omit in toc -->

- [Introduction](#introduction)
- [Decentralized Identity / Self-Sovereign Identity](#decentralized-identity--self-sovereign-identity)
  - [Open Standards](#open-standards)
    - [Decentralized Identifiers (DID)](#decentralized-identifiers-did)
    - [Verifiable Credentials](#verifiable-credentials)
    - [Links to Emerging DID and Verifiable Credentials Standards](#links-to-emerging-did-and-verifiable-credentials-standards)
      - [DID Standards](#did-standards)
      - [Verifiable Credentials Standards](#verifiable-credentials-standards)
  - [General Model](#general-model)
  - [Technology](#technology)
    - [Distributed Ledger Technology / Blockchain](#distributed-ledger-technology--blockchain)
    - [Decentralized Key Management Systems](#decentralized-key-management-systems)
    - [Zero Knowledge Proofs](#zero-knowledge-proofs)
  - [Summary: Decentralized Identity / Self-Sovereign Identity Architecture](#summary-decentralized-identity--self-sovereign-identity-architecture)
- [Hyperledger Indy](#hyperledger-indy)
  - [Overview](#overview)
  - [Technical information for Hyperledger Indy](#technical-information-for-hyperledger-indy)
- [Hyperledger Indy Catalyst](#hyperledger-indy-catalyst)
  - [Motivation](#motivation)
  - [Who is Indy Catalyst For](#who-is-indy-catalyst-for)
  - [Key Technical Elements](#key-technical-elements)
    - [Credential Registry](#credential-registry)
    - [Agent](#agent)
    - [Agent Driver](#agent-driver)
    - [Starter Kits](#starter-kits)
      - [Credential Registry Holder-Prover](#credential-registry-holder-prover)
      - [Agent Issuer-Verifier](#agent-issuer-verifier)
- [Endnotes](#endnotes)

# Introduction

## Getting Started

The best way to get started is with a working application.  The [Quick Start Guide](./docker/README.md#running-a-complete-provisional-von-network) for **Running a Complete Provisional VON Network** will get you started with a complete set of applications running on your local machine in Docker.

## Running on OpenShift

In order to understand the goals and context of Hyperledger Indy Catalyst, it is advisable to become familiar with the model of decentralized identity or self-sovereign identity which enables trustworthy entity to entity communications. The open standards and technologies enabling this new this model are presented below and annotated with references.

# Decentralized Identity / Self-Sovereign Identity

The project can also be run locally using Docker and Docker Compose.  Refer to [Running TheOrgBook with Docker Compose](./docker/README.md) for instructions.

## Resetting the Ledger

For information on the process of resetting the ledger and wallets refer to the [Resetting the Ledger and Wallets](./ResettingTheLedger.md) documentation.