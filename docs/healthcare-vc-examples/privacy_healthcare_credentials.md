# Privacy & Compliance Notes for Health Credentials (Non-PHI)
## PHI Minimization
- Do not include diagnoses, notes, lab values, prescriptions, or free-text clinical content.
- Use coarse enums and timestamps; omit narrative details.

## Selective Disclosure
- Prefer schemas compatible with ZK/AnonCreds-style selective disclosure.
- Keep attributes simple and independently disclosable.

## Revocation & Rotation
- Support credential revocation lists.
- Document issuer DID key rotation procedures.

## Data Residency & Retention
- Store PHI off-chain under appropriate legal frameworks (HIPAA/GDPR).
- Place only minimal proofs or anonymized claims in credentials.

