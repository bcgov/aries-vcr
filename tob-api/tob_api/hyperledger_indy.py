import os
import platform

def config():
    genesis_txn_path = "/opt/app-root/genesis"
    platform_name = platform.system()
    if platform_name == "Windows":
        genesis_txn_path = os.path.realpath("./app-root/genesis")
    
    return {
        "genesis_txn_path": genesis_txn_path,
    }
