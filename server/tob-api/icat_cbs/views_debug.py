import logging
import os
import uuid

from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import permissions
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response

from icat_cbs.utils.credential import Credential, CredentialManager

LOGGER = logging.getLogger(__name__)


@swagger_auto_schema(
    method="post",
    request_body=openapi.Schema(
        type=openapi.TYPE_OBJECT,
        properties={
            "raw_credential": openapi.Schema(
                type=openapi.TYPE_OBJECT,
                properties={
                    "schema_id": openapi.Schema(
                        type=openapi.TYPE_STRING, description="string"
                    ),
                    "cred_def_id": openapi.Schema(
                        type=openapi.TYPE_STRING, description="string"
                    ),
                    "values": openapi.Schema(
                        type=openapi.TYPE_OBJECT,
                        properties={
                            "valN": openapi.Schema(
                                type=openapi.TYPE_OBJECT,
                                properties={
                                    "raw": openapi.Schema(
                                        type=openapi.TYPE_STRING, description="string"
                                    )
                                },
                            )
                        },
                    ),
                },
            )
        },
    ),
)
@api_view(["POST"])
@permission_classes((permissions.AllowAny,))
def receive_credential(request):
    """
    Receive a stripped-down credential and store it in the credential registry.
    This endpoint is for testing/debug purposes ONLY!

    To issue a credential:
    - use the */api/v2/credentialtype* endpoint to determine the _cred_def_id_,
    - use the */api/v2/schema* endpoint to build the _schema_id_ in the form _origin_did:id:name:version_
    - add the relevant attributes in the values object, using the value name as key instead of _valN_ and the string value as its _raw_ value
    - call this API
    """
    message = request.data
    credential_id = uuid.uuid4()
    raw_credential = message["raw_credential"]

    LOGGER.debug("Received raw-credential: {}".format(raw_credential))

    credential_data = {
        "schema_id": raw_credential["schema_id"],
        "cred_def_id": raw_credential["cred_def_id"],
        "rev_reg_id": credential_id,  # we use the same value as credential_id
        "attrs": raw_credential["values"],
    }

    for attr in raw_credential["values"]:
        credential_data["attrs"][attr] = raw_credential["values"][attr]["raw"]

    try:
        credential = Credential(
            credential_data, credential_id=credential_id
        )

        credential_manager = CredentialManager()
        credential_manager.process(credential)
    except Exception as e:
        LOGGER.error("An exception occurred while processing the credential:")
        LOGGER.error(str(e))
        return Response({"success": False, "error": str(e)})

    return Response({"success": True})
