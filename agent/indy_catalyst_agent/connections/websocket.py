class WebsocketConnection:
    def __init__(self, send):
        self.send = send

    async def send_message(self, message):
        """
        Send a message to this connection
        """
        await self.send(message.serialize())
