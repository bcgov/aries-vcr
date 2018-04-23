import json
import random
from string import ascii_lowercase, digits

import base58
from django.contrib.auth.models import Group
from didauth.base import KeyFinderBase, VerifierException
from didauth.headers import HeaderVerifier

from api.indy.agent import Verifier
from api.eventloop import do as run_loop
from .models import User


ISSUERS_GROUP_NAME = 'issuers'


def get_issuers_group():
    group, _created = Group.objects.get_or_create(name=ISSUERS_GROUP_NAME)
    return group


def generate_random_username(length=16, chars=ascii_lowercase+digits, split=4, delimiter='-', prefix=''):
    username = ''.join([random.choice(chars) for i in range(length)])
    
    if split:
        username = delimiter.join([username[start:start+split] for start in range(0, len(username), split)])
    username = prefix + username
    
    try:
        User.objects.get(username=username)
        return generate_random_username(length=length, chars=chars, split=split, delimiter=delimiter)
    except User.DoesNotExist:
        return username


class DidAuthKeyFinder(KeyFinderBase):
    def find_key(self, key_id: str, key_type: str):
        assert key_type == 'ed25519'
        if key_id.startswith('did:sov:'):
            key_id = key_id[8:]
        async def fetch_key():
            async with Verifier() as verifier:
                nym = await verifier.get_nym(key_id)
                nym = json.loads(nym) if nym else None
                if not nym:
                    return None
                return base58.b58decode(nym['verkey'])
        return run_loop(fetch_key())


class DidAuthBackend:
    """
    Authenticate a user based on the DID-Auth HTTP Signature
    """

    def authenticate(self, request):
        result = None
        try:
            verified = verify_signature(request.META)
        except HttpSigException as e:
            print(e)
            verified = None
        if verified:
            try:
                result = User.objects.get(DID=verified['keyId'])
            except User.DoesNotExist:
                # must register via register-issuer
                result = None
        return result

    def get_user(self, user_id):
        try:
            return User.objects.get(pk=user_id)
        except User.DoesNotExist:
            return None


def revert_header_name(hdr):
    if hdr.startswith('HTTP_'):
        hdr = hdr[5:]
    elif hdr != 'CONTENT_LENGTH' and hdr != 'CONTENT_TYPE':
        return None
    return hdr.lower().replace('_', '-')


def verify_signature(request):
    raw_headers = {}
    for (key,val) in request.META.items():
        target = revert_header_name(key)
        if target:
            raw_headers[target] = val
    verifier = HeaderVerifier(DidAuthKeyFinder())
    path = request.path
    qs = request.META['QUERY_STRING']
    if qs:
        path += '?' + qs
    return verifier.verify(raw_headers, path=path, method=request.method)
