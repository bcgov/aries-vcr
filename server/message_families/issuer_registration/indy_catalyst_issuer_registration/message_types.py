"""Message type identifiers for Issuer Registrations."""

from aries_cloudagent.protocols.didcomm_prefix import DIDCommPrefix

ARIES_PROTOCOL = "issuer-registration/1.0"

# Message types
REGISTER = f"{ARIES_PROTOCOL}/register"

PROTOCOL_PACKAGE = "indy_catalyst_issuer_registration"

MESSAGE_TYPES = DIDCommPrefix.qualify_all(
    {
        REGISTER: f"{PROTOCOL_PACKAGE}.messages.register.IssuerRegistration"
    }
)
