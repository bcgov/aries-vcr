"""Message type identifiers for Connections."""

MESSAGE_FAMILY = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/credential-presentation/0.1"

PRESENTATION_REQUEST = f"{MESSAGE_FAMILY}/presentation-request"
CREDENTIAL_PRESENTATION = f"{MESSAGE_FAMILY}/credential-presentation"

MESSAGE_TYPES = {
    PRESENTATION_REQUEST: (
        "indy_catalyst_agent.messaging.presentations.messages."
        + "presentation_request.PresentationRequest"
    ),
    CREDENTIAL_PRESENTATION: (
        "indy_catalyst_agent.messaging.presentations.messages."
        + "credential_presentation.CredentialPresentation"
    ),
}
