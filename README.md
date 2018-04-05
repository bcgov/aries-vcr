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

**Hyperledger Indy Catalyst** is a set of application level software components designed to accelerate the adoption of trustworthy entity to entity<sup id="a1">[1](#f1)</sup> communications based on Decentralized Identity / Self-Sovereign Identity technology and architecture. Indy Catalyst is builds upon globally available open standards and open source software. At present, Indy Catalyst builds upon [Hyperledger Indy](https://www.hyperledger.org/projects), common enterprise open source software, frameworks and patterns such as PostgreSQL, Python, Angular and RESTful APIs. Efforts will be taken to design the software to facilitate the incorporation of evolving open standards and technology. The impetus for Indy Catalyst came from the Verifiable Organizations Network (VON) project. More information about VON can be found at [vonx.io](https://vonx.io)

In order to understand the goals and context of Hyperledger Indy Catalyst, it is advisable to become familiar with the model of decentralized identity or self-sovereign identity which enables trustworthy entity to entity communications. The open standards and technologies enabling this new this model are presented below and annotated with references.

# Decentralized Identity / Self-Sovereign Identity

The project can also be run locally using Docker and Docker Compose.  Refer to [Running TheOrgBook with Docker Compose](./docker/README.md) for instructions.

## Resetting the Ledger

For information on the process of resetting the ledger and wallets refer to the [Resetting the Ledger and Wallets](./ResettingTheLedger.md) documentation.