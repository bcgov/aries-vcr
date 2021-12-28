![Hyperledger Aries VCR](/docs/assets/aries-vcr-logo.jpg)

[![License](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](./LICENSE)
[![Lifecycle:Stable](https://img.shields.io/badge/Lifecycle-Stable-97ca00)](./README.md)

## Overview

Aries Verifiable Credentials Registry (VCR), part of the [Hyperledger Aries](https://www.hyperledger.org/use/aries) family of Digital Trust technologies, provides a searchable public directory based on Verifiable Credentials (VCs). It was historically known as both OrgBook (which is actually a deployment of Aries VCR) and Indy Catalyst.

Aries VCR is actively developed by the British Columbia Government’s Digital Trust Team in Canada, and the most well-known live example is [OrgBook BC](https://www.orgbook.gov.bc.ca/en/home).

In an instance of Aries VCR, credentials can be issued from a variety of authorities about subjects in the instance. A core set of credentials are issued by an authority responsible for “creating” the subject. Other credentials can then be issued against the subject of these core credentials. All credentials are stored in a secure digital wallet and accessed via its website or the public API. This means an instance of Aries VCR can be an authoritative public registry of any referenceable information.

![A diagram showing the relationship between issuing organizations and Aries VCR, including ways to consume Aries VCR data via the website and API](/docs/assets/aries-vcr-architecture-diagram.png)


An instance of Aries VCR also differs from a traditional database in several additional ways, including:
* Credentials stored in Aries VCR are tamperproof, so any attempt to change the data would be detected
* Any user can prove exactly which issuer issued a credential, and the issuer doesn’t need to be contacted to make that proof
* Credentials are cryptographically encrypted when being issued and stored.

Aries VCR is built using open source technologies, and is based on [Aries Cloud Agent Python (ACA-Py)](https://github.com/hyperledger/aries-cloudagent-python), a flexible, open-source Aries framework for Digital Trust that’s under continuous and active development. In the four-layer [Trust Over IP framework (PDF)](https://trustoverip.org/wp-content/uploads/sites/98/2020/05/toip_050520_primer.pdf) Aries VCR sits in the third layer, Trusted Exchanges.

For practical usage, issuers issue their credentials to an instance of Aries VCR using a standard web controller with business logic, such as with the template [Aries VCR Issuer Controller](https://github.com/bcgov/aries-vcr-issuer-controller).

Users can access data in an instance of Aries VCR through:
* A searchable website interface, instantly familiar to any web users and fully customizable for any branding or design
* An API, allowing developers to use the data in any way they need.

## Example Applications and Live Services

A well-known live Aries VCR instance is [OrgBook BC](https://www.orgbook.gov.bc.ca/en/home), a directory containing organizations registered in British Columbia, Canada, as well as licenses and permits issued to those organizations.

### Example 1: Business registration

OrgBook BC is a business registration application of Aries VCR. Information about government-registered corporations (name, registration ID, address, directors, and so forth) is the root of trust in an instance of Aries VCR, and then business permits, liquor licenses, and so forth are issued against those corporations. Citizens, organizations and others could then look up a corporation and see up-to-date, proven information and any associated licenses and permits.

### Example 2: Vaccination and testing locations

In this application, the root of trust would be government information on approved labs and health sites in a region or across the country. Then, a government regulatory agency would issue credentials against specific locations that are authorized to deliver particular vaccinations and tests.

### Example 3: Educational institutions

A national or international registry of educational institutions is a third example. The root of trust might be a regional government (or whoever has oversight of educational institutions) issuing credentials about all diploma-granting institutions. Those credentials could include details about the specific diplomas they’re authorized to grant and the identifier (DID) each institution uses in issuing diploma credentials to individuals.

The model could be extended with another layer or two. For example, it could extend to a national entity issuing credentials about the authority of the regional oversight bodies. And to make it international in scope, a global authority could issue credentials about the national authority.

## How to get started

Aries VCR uses standard technologies and common integration patterns. If you’re a developer it should be a relatively minimal effort to get up and running.

If you simply want to see an Aries VCR instance in action, you can try out the [OrgBook BC search interface](https://www.orgbook.gov.bc.ca/en/home).

Alternatively, if you are just wanting to issue credentials to an existing Aries VCR installation then you need the [Aries VCR Issuer Controller](https://github.com/bcgov/aries-vcr-issuer-controller) repo.

If you wish to create your own instance of Aries VCR, read on.

You will need:
1. A Hyperledger Indy-compatible ledger to store issuer DIDs and credential schemas. For development, you can use [VON Network](https://github.com/bcgov/von-network) to run a local Indy instance. For production, you might use a global Indy instance, such as the one run by the [Sovrin Foundation](https://sovrin.org).
2. This repo, run in Docker on a local machine to start.
3. (Optional) An issuer controller that issues credentials to your Aries VCR instance.

This repo has [setup instructions](https://github.com/bcgov/aries-vcr/blob/main/docs/README.md) for these three steps (using some old terminology in places).

If you wish to explore the API, a great starting place is the [API web interface for OrgBook BC](https://orgbook.gov.bc.ca/api/), presented using Swagger. Also, this [API repo](https://github.com/bcgov/orgbook-api) has a demo of how you can use the REST API to access Aries VCR credentials.

For the client (web) interface, the search is powered by [Solr](https://solr.apache.org). The user interface is fully customizable; this repo has instructions on [customizing the interface and theme](https://github.com/bcgov/aries-vcr/blob/main/client/ThemeDevelopment.md).

Aries VCR also provides a [web hook facility](https://github.com/bcgov/aries-vcr/blob/main/docs/Subscription-Web-Hooks.md) so parties can subscribe to notifications for credential updates. It is possible to subscribe to all new credentials, any updates to existing credentials, or updates to specific credentials.

## Credit

Aries VCR was developed by the Government of British Columbia’s Digital Trust Team.

## Contributing

Pull requests are welcome! Please read our [contributions guide](https://github.com/bcgov/aries-vcr/blob/main/CONTRIBUTING.md) and submit your PRs. We enforce [developer certificate of origin](https://developercertificate.org) (DCO) commit signing—[guidance](https://github.com/apps/dco) is available on how to achieve that.

We also welcome issues submitted about problems you encounter in using Aries VCR.

## License

[Apache License Version 2.0](https://github.com/bcgov/aries-vcr/blob/main/LICENSE)
