import os
import platform
import requests
from pathlib import Path

import logging
logger = logging.getLogger(__name__)


def getGenesisData():
    """
    Get a copy of the genesis transaction file from the web.
    """
    ledgerUrl = os.getenv('LEDGER_URL').lower()
    if not ledgerUrl:
        raise Exception('LEDGER_URL must be set.')
    logger.info('Using genesis transaction file from {}/genesis'.format(ledgerUrl))
    response = requests.get('{}/genesis'.format(ledgerUrl))
    return response.text

def checkGenesisFile(genesis_txn_path):
    """
    Check on the genesis transaction file and create it is it does not exist.
    """
    genesis_txn_file = Path(genesis_txn_path)
    if not genesis_txn_file.exists():
        if not genesis_txn_file.parent.exists():
          genesis_txn_file.parent.mkdir(parents = True)
        data = getGenesisData()
        with open(genesis_txn_path, 'x') as genesisFile:
            genesisFile.write(data)

def config():
    """
    Get the hyperledger configuration settings for the environment.
    """
    genesis_txn_path = "/opt/app-root/src/genesis"
    platform_name = platform.system()
    if platform_name == "Windows":
        genesis_txn_path = os.path.realpath("./app-root/src/genesis")
    
    checkGenesisFile(genesis_txn_path)

    return {
        "genesis_txn_path": genesis_txn_path,
    }
