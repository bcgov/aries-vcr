"""Message type identifiers for Issuer Registrations."""

DID_PREFIX = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec";
MESSAGE_FAMILY = "/issuer-registration/1.0"

MESSAGE_TYPE = f"{MESSAGE_FAMILY}/register"

REGISTER = f"{DID_PREFIX}/{MESSAGE_FAMILY}{MESSAGE_TYPE}"

MESSAGE_TYPES = {
    REGISTER: "indy_catalyst_issuer_registration."
    + "messages.register.IssuerRegistration"
}
