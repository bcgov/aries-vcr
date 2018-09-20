# Using the CLI

You can run the CLI as follows:

```
docker exec -it <tob-api docker image> bash
indy-cli
```

... or you can run the indy CLI locally (check the indy-sdk for instructions to build or install), or from any docker container that is build based on the von-image base image.  (von-image contains the indy-cli)

Note that you can use "help" to get more info for any command, for example:

```
help
wallet help
pool create help
```

... Etc.

## Creating DID's in a Local Wallet

You need a wallet to start creating DID's.  Create a local SQLite wallet with the following CLI commands:

```
wallet create my_wallet key
wallet open my_wallet key
```

The CLI will prompt you for the actual "key" - you can use whatever you want, but make sure you type in the same value when you create and open the wallet.  If you forget the "key", you will not be able to open the wallet!

To create a DID, for example from a seed:

```
did new seed=000000000000000000000000Trustee1
did new seed=00000000000000000000000087654321
did list
```

The first DID is the Trustee created by default in VON-Network, and is required if you want to write anything to the (VON-Network) ledger.  Make a note of the DID that is created from the "trustee" seed!

## Connecting to a Ledger

First get a hold of the genesis file for your ledger, and save it somewhere locally (for example save it to "/tmp/genesis.json").  You can download the VON-Network genesis file from, for example, "http://159.89.115.24/genesis" (this is the Dev network).

Then create a pool and connect to the ledger with the following CLI commands (substitute your own pool name and genesis file location):

```
pool create my_pool gen_txn_file=/tmp/genesis.json
pool connect my_pool
```

If you are connecting to an older pool you can use:

```
pool connect my_pool protocol-version=1
```

## Writing DID's to a Ledger

First you need to "did use" to enable the Trustee role:

```
did use <the trustee DID>
```

If you can't remember the Trustee DID, you can run "did list".

Then, to write a DID to the ledger:

```
ledger nym did=<something> verkey=<~something else>
ledger nym did=<something> role=<???>
```

There are other options, check out "ledger nym help".  If you get an error message you probably "did used" the wrong DID.

## Connecting to a Postgres Wallet

To connect to a postgres wallet you need to know the url of the postgres server, as well as the account and password to connect.  

For example the following assumes the postres wallet already exists (for example was created by TOB):

```
wallet create tob_holder key storage_type=postgres storage_config={"url":"wallet-db:5432"} storage_credentials={"account":"postgres","password":"mysecretpassword"}
wallet open tob_holder key storage_credentials={"account":"postgres","password":"mysecretpassword"}
```

If you are actually creating a new wallet you also need to provide a postgres admin account:

```
wallet create tob_new key storage_type=postgres storage_config={"url":"wallet-db:5432"} storage_credentials={"account":"postgres","password":"mysecretpassword","admin-account":"postgres","admin-password":"mysecretpassword"}
wallet open tob_new key storage_credentials={"account":"postgres","password":"mysecretpassword"}
```

## Rotating a Wallet's Encryption Keys

To rotate the encryption key you need to specify both "key" and "rekey" when you open the wallet:

```
# enter the old "key" and the new "rekey":
wallet open tob_holder key rekey storage_credentials={"account":"postgres","password":"mysecretpassword"}
wallet close tob_holder

# now use the "rekey" from above as the new "key":
wallet open tob_holder key storage_credentials={"account":"postgres","password":"mysecretpassword"}
```

Note that you are prompted for the "key" and "rekey" values.  Remember the latest value as you need it to open the wallet!  (I.e. the value you enter for "rekey" is the value you need to use for "key" next time you open the wallet.)

## Exporting and Importing a Wallet

Easy peasy - this example exports from Postgres and imports into SQLite:

```
wallet open ... (whatever wallet you want to export)
wallet export export_path=/tmp/wallet_export_file export_key
wallet close ...
```

You create the new wallet on import, so you need to provide all the same info as in "wallet create ...".

For SQLite:

```
wallet import new_wallet key export_path=/tmp/wallet_export_file export_key
```

... but for Postgres:

```
wallet import new_wallet key export_path=/tmp/wallet_export_file export_key storage_config={"url":"wallet-db:5432"} storage_credentials={"account":"postgres","password":"mysecretpassword","admin-account":"postgres","admin-password":"mysecretpassword"}
```

... and you need the admin credentials, because import needs to create a new wallet.
