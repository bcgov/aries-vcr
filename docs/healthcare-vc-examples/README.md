# Healthcare Verifiable Credential Examples (Non-PHI)
Purpose: Provide minimal, privacy-preserving VC examples suitable for health-related use cases without handling Protected Health Information (PHI).

Included:
- MentalWellnessSessionCredential — attendance proof without content details.
- PractitionerAttestationCredential — practitioner status attestation with revocation support.

Design principles:
- PHI minimization
- Selective disclosure friendly attributes
- Revocation and key rotation awareness

## Repository fit and usage
These non-PHI healthcare credential examples are intended as reference artifacts for Aries VCR adopters. They demonstrate minimal, privacy-preserving schemas that can be issued by healthcare-related verifiers and later presented to relying parties through standard Aries components. They are not personal wallet personas; they are reusable templates showing how to model attendance and practitioner attestation in a way that avoids PHI while supporting revocation and selective disclosure.
