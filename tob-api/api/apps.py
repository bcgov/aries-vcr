import json
from datetime import datetime
import os

import requests

from api.indy.agent import Holder
from . import eventloop

from django.apps import AppConfig

import logging
logger = logging.getLogger(__name__)


# TODO fix this global variable, badly implemented :-(
def get_remote_wallet_token():
    return remote_wallet_token
remote_wallet_token = None

class apiConfig(AppConfig):
    name = 'api'

    def ready(self):
        now = datetime.now().strftime("%Y-%m-%d")

        async def run():
            # If wallet type is "remote" then login to get  token
            WALLET_TYPE = os.environ.get('INDY_WALLET_TYPE')
            if WALLET_TYPE == 'remote':
            	WALLET_USERID = 'wall-e'    # TODO hardcode for now
            	WALLET_PASSWD = 'pass1234'  # TODO hardcode for now
            	WALLET_BASE_URL = os.environ.get('INDY_WALLET_URL')
            	print("Wallet URL: " + WALLET_BASE_URL)

    	        try:
    	            my_url = WALLET_BASE_URL + "api-token-auth/"
    	            response = requests.post(my_url, data = {"username":WALLET_USERID, "password":WALLET_PASSWD})
    	            json_data = response.json()
    	            remote_token = json_data["token"]
    	            print("Authenticated remote wallet server: " + remote_token)
    	        except:
    	            raise Exception(
    	                'Could not login to wallet. '
    	                'Is the Wallet Service running?')
            else:
                remote_token = None

            return remote_token

        # TODO fix must be a better way
        global remote_wallet_token
        remote_wallet_token = eventloop.do(run())

