"""Message type identifiers for Connections."""

MESSAGE_FAMILY = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credentials/1.0/"

CREDENTIAL_OFFER = f"{MESSAGE_FAMILY}credential_offer"
CREDENTIAL_REQUEST = f"{MESSAGE_FAMILY}credential_request"
CREDENTIAL = f"{MESSAGE_FAMILY}credential"

MESSAGE_TYPES = {
    CREDENTIAL_OFFER: (
        "indy_catalyst_agent.messaging.credentials.messages."
        + "credential_offer.CredentialOffer"
    ),
    CREDENTIAL_REQUEST: (
        "indy_catalyst_agent.messaging.credentials.messages."
        + "credential_request.CredentialRequest"
    ),
    CREDENTIAL: (
        "indy_catalyst_agent.messaging.credentials.messages." + "credential.Credential"
    ),
}
