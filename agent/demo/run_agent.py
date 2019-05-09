import subprocess
import time
import urllib.request, urllib.parse
import threading
import os
import requests
import random


def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        #print('got line: {0}'.format(line.decode('utf-8')), end='')
        pass


def stderr_reader(proc):
    for line in iter(proc.stderr.readline, b''):
        #print('got line: {0}'.format(line.decode('utf-8')), end='')
        pass


def main():
    """
PYTHONPATH=.. ../scripts/icatagent \
            --inbound-transport http 0.0.0.0 8000 \
            --inbound-transport http 0.0.0.0 8001 \
            --inbound-transport ws 0.0.0.0 8002 \
            --outbound-transport ws \
            --outbound-transport http \
            --admin localhost 8080
    """
    my_env = os.environ.copy()
    my_env["PYTHONPATH"] = ".."

    # TODO figure out how to start and expose a REST callback service
    my_env["WEBHOOK_URL"] = "TBD"

    # TODO genesis transactions from file or url
    with open('local-genesis.txt', 'r') as genesis_file:
        genesis = genesis_file.read()
    #print(genesis)

    # TODO seed from input parameter; optionally register the DID
    rand_name = str(random.randint(100000, 999999))
    seed = ('my_seed_000000000000000000000000' + rand_name)[-32:]
    alias = 'My Test Company'
    register_did = True
    if register_did:
        print("Registering", alias, "with seed", seed)
        ledger_url = 'http://localhost:9000'
        headers = {"accept": "application/json"}
        data = {"alias": alias, "seed": seed, "role": "TRUST_ANCHOR"}
        resp = requests.post(ledger_url+'/register', json=data)
        nym_info = resp.text
        print(nym_info)

    # start agent sub-process
    proc = subprocess.Popen(['python3', '../scripts/icatagent', 
                            '--inbound-transport', 'http', '0.0.0.0', '8000', 
                            '--inbound-transport', 'http', '0.0.0.0', '8001', 
                            '--inbound-transport', 'ws', '0.0.0.0', '8002',
                            '--outbound-transport', 'ws', 
                            '--outbound-transport', 'http', 
                            '--auto-respond-messages',
                            '--genesis-transactions', genesis,
                            '--wallet-type', 'indy',
                            '--wallet-name', 'faber'+rand_name,
                            '--wallet-key', 'faber'+rand_name,
                            '--seed', seed,
                            '--admin', '0.0.0.0', '8080'],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=my_env)
    time.sleep(0.5)
    t1 = threading.Thread(target=output_reader, args=(proc,))
    t1.start()
    t2 = threading.Thread(target=stderr_reader, args=(proc,))
    t2.start()
    time.sleep(3.0)
    try:
        time.sleep(0.2)

        # check swagger content
        resp = requests.get('http://localhost:8080/api/docs/swagger.json')
        p = resp.text
        assert 'Indy Catalyst Agent' in p

        # create a schema
        version = format("%d.%d.%d" % (random.randint(1, 101), random.randint(1, 101), random.randint(1, 101)))
        schema_body = {
                "schema_name": "iiw_attendance",
                "schema_version": version,
                "attributes": ["email", "full_name", "time"],
            }
        schema_response = requests.post(f"http://localhost:8080/schemas", json=schema_body)
        print(schema_response.text)
        schema_response_body = schema_response.json()
        schema_id = schema_response_body["schema_id"]
        print(schema_id)

        # create a cred def for the schema
        credential_definition_body = {"schema_id": schema_id}
        credential_definition_response = requests.post(
            f"http://localhost:8080/credential-definitions", json=credential_definition_body
        )
        credential_definition_response_body = credential_definition_response.json()
        credential_definition_id = credential_definition_response_body[
            "credential_definition_id"
        ]

        print(f"cred def id: {credential_definition_id}")

        # generate an invitation
        headers = {"accept": "application/json"}
        resp = requests.post('http://localhost:8080/connections/create-invitation', headers=headers)
        p = resp.text
        print("*****************")
        print("Invitation:", p)
        print("*****************")

    except Exception as e:
        print(e)
    finally:
        time.sleep(2.0)
        print("waiting ...")
        val = input("<Enter> to Exit :-D") 
        proc.terminate()
        try:
            proc.wait(timeout=0.5)
            print('== subprocess exited with rc =', proc.returncode)
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')
    t1.join()
    t2.join()

if __name__ == "__main__":
    main()
