"""Register default routes."""

from aiohttp import web

from ..messaging.connections.routes import register as register_connections
from ..messaging.credentials.routes import register as register_credentials
from ..messaging.schemas.routes import register as register_schemas
from ..messaging.credential_definitions.routes import (
    register as register_credential_definitions,
)


async def register_module_routes(app: web.Application):
    """
    Register default routes with the webserver.

    Eventually this should use dynamic registration based on the
    selected message families.
    """
    await register_connections(app)
    await register_credentials(app)
    await register_schemas(app)
    await register_credential_definitions(app)
