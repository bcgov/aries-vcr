"""Message type identifiers for Connections."""

MESSAGE_FAMILY = "did:sov:BzCbsNYhMrjHiqZDTUASHg;spec/basicmessage/1.0"

BASIC_MESSAGE = f"{MESSAGE_FAMILY}/message"

MESSAGE_TYPES = {
    BASIC_MESSAGE: "indy_catalyst_agent.messaging.basicmessage."
    + "messages.basicmessage.BasicMessage"
}
