import json
import logging
import random
from string import ascii_lowercase, digits

import base58
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType
from didauth.base import KeyFinderBase
from didauth.error import VerifierException
from didauth.headers import HeaderVerifier
from rest_framework import authentication, exceptions, permissions

from api.models.User import User
from api.models.VerifiableClaim import VerifiableClaim

from tob_anchor.boot import indy_client, indy_verifier_id
from vonx.common.eventloop import run_coro

ISSUERS_GROUP_NAME = "issuers"


def create_issuer_user(
    email,
    issuer_did,
    username=None,
    password=None,
    display_name="",
    first_name="",
    last_name="",
    verkey=None,
):
    logger = logging.getLogger(__name__)
    try:
        user = User.objects.get(DID=issuer_did)
    except User.DoesNotExist:
        logger.debug("Creating user for DID '{0}' ...".format(issuer_did))
        if not username:
            username = generate_random_username(
                length=12, prefix="issuer-", split=None
            )
        user = User.objects.create_user(
            username,
            email=email,
            password=password,
            DID=issuer_did,
            verkey=verkey,
            display_name=display_name,
            first_name=first_name,
            last_name=last_name,
        )
        user.groups.add(get_issuers_group())
    else:
        user.DID = issuer_did
        user.verkey = verkey
        user.email = email
        user.display_name = display_name
        if first_name != None:
            user.first_name = first_name
        if last_name != None:
            user.last_name = last_name
        user.save()
    return user


def get_issuers_group():
    group, created = Group.objects.get_or_create(name=ISSUERS_GROUP_NAME)
    if created:
        claims_type = ContentType.objects.get_for_model(VerifiableClaim)
        create_claims_perm = Permission.objects.get(
            content_type=claims_type, codename="add_verifiableclaim"
        )
        group.permissions.add(create_claims_perm)
    return group


def generate_random_username(
    length=16,
    chars=ascii_lowercase + digits,
    split=4,
    delimiter="-",
    prefix="",
):
    username = "".join([random.choice(chars) for i in range(length)])

    if split:
        username = delimiter.join(
            [
                username[start : start + split]
                for start in range(0, len(username), split)
            ]
        )
    username = prefix + username

    try:
        User.objects.get(username=username)
        return generate_random_username(
            length=length, chars=chars, split=split, delimiter=delimiter
        )
    except User.DoesNotExist:
        return username


class IsRegisteredIssuer(permissions.BasePermission):
    def has_permission(self, request, view):
        return (
            request.user
            and request.user.groups.filter(name=ISSUERS_GROUP_NAME).exists()
        )


class CanStoreClaims(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user and request.user.has_perm(
            "api.add_verifiableclaim"
        )


class IsSignedRequest(permissions.BasePermission):
    def has_permission(self, request, view):
        if verify_signature(request):
            return True
        return False


class DidAuthKeyFinder(KeyFinderBase):
    """
    Look up the public key for an issuer, first in the Users table then in the ledger
    """

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def find_key(self, key_id: str, key_type: str):
        assert key_type == "ed25519"
        if key_id.startswith("did:sov:"):
            short_key_id = key_id[8:]
        else:
            short_key_id = key_id
            key_id = "did:sov:" + short_key_id
        try:
            user = User.objects.get(DID=key_id)
            if user.verkey:
                verkey = bytes(user.verkey)
                self.__logger.debug(
                    "Found verkey for DID '{}' in users table: '{}'".format(
                        key_id, verkey
                    )
                )
                return verkey
        except User.DoesNotExist:
            pass

        async def fetch_key():
            self.__logger.debug(
                "Fetching verkey for DID '{}' from ledger".format(key_id))
            nym_info = await indy_client().resolve_nym(short_key_id, indy_verifier_id())
            if not nym_info.data:
                return None
            return base58.b58decode(nym_info.data['verkey'])
        return run_coro(fetch_key())


class DidAuthentication(authentication.BaseAuthentication):
    """
    rest_framework authentication backend
    Authenticate a user based on the DID-Auth HTTP Signature
    """

    def __init__(self):
        self.__logger = logging.getLogger(__name__)

    def authenticate(self, request):
        self.__logger.info("Authenticating DID...")
        result = None
        try:
            verified = verify_signature(request)
        except VerifierException as e:
            # bad signature present - fail explicitly
            verified = None
            self.__logger.warn(
                "Exception when authorizing DID signature: %s", e
            )
            raise exceptions.AuthenticationFailed(
                "Exception when authorizing DID signature: %s" % (e,)
            )
        if verified:
            try:
                user = User.objects.get(DID=verified["keyId"])
                result = (user, verified)
            except User.DoesNotExist:
                self.__logger.warn(
                    "DID authenticated but user not found: %s",
                    verified["keyId"],
                )
                # may be in the process of registering
        else:
            self.__logger.warn("No DID signature")
        return result


def revert_header_name(hdr):
    if hdr.startswith("HTTP_"):
        hdr = hdr[5:]
    elif hdr != "CONTENT_LENGTH" and hdr != "CONTENT_TYPE":
        return None
    return hdr.lower().replace("_", "-")


def verify_signature(request, key_finder=None):
    verified = request.META.get("SIGNATURE")
    if verified is not None:
        return verified
    raw_headers = {}
    for (key, val) in request.META.items():
        target = revert_header_name(key)
        if target:
            raw_headers[target] = val
    verifier = HeaderVerifier(key_finder or DidAuthKeyFinder())
    path = request.path  # maybe prefer request.META['RAW_URI']
    qs = request.META["QUERY_STRING"]
    if qs:
        path += "?" + qs
    log = logging.getLogger(__name__)
    log.debug(
        "didauth %s '%s', headers: %r", request.method, path, raw_headers
    )
    try:
        verified = verifier.verify(
            raw_headers, path=path, method=request.method
        )
    except VerifierException:
        request.META["SIGNATURE"] = False
        raise
    request.META["SIGNATURE"] = verified
    if verified:
        request.META["VERIFIED_DID"] = verified["keyId"]
    return verified
