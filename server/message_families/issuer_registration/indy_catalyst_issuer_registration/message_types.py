"""Message type identifiers for Issuer Registrations."""

DID_PREFIX = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec";
MESSAGE_FAMILY = f"{DID_PREFIX}/issuer-registration/1.0"

REGISTER = f"{MESSAGE_FAMILY}/register"

MESSAGE_TYPES = {
    REGISTER: "indy_catalyst_issuer_registration."
    + "messages.register.IssuerRegistration"
}
