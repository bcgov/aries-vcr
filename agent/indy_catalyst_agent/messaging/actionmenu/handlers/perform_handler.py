"""Action menu perform request message handler."""

from ...base_handler import BaseHandler, BaseResponder, RequestContext
from ..base_service import BaseMenuService
from ..messages.perform import Perform


class PerformHandler(BaseHandler):
    """Message handler class for action menu perform requests."""

    async def handle(self, context: RequestContext, responder: BaseResponder):
        """
        Message handler logic for action menu perform requests.

        Args:
            context: request context
            responder: responder callback
        """
        self._logger.debug(f"PerformHandler called with context {context}")
        assert isinstance(context.message, Perform)

        self._logger.info("Received action menu perform request")

        service: BaseMenuService = await context.inject(BaseMenuService, required=False)
        if service:
            reply = await service.perform_menu_action(
                context.message.name,
                context.message.params or {},
                context.connection_record,
                context.message._thread_id,
            )
            if reply:
                await responder.send_reply(reply)
        else:
            # send problem report?
            pass
