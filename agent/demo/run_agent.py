import subprocess
import time
import urllib.request, urllib.parse
import threading
import os
import requests
import random


def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        print('got line: {0}'.format(line.decode('utf-8')), end='')


def stderr_reader(proc):
    for line in iter(proc.stderr.readline, b''):
        print('got line: {0}'.format(line.decode('utf-8')), end='')


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

    with open('local-genesis.txt', 'r') as genesis_file:
        genesis = genesis_file.read()
    print(genesis)

    proc = subprocess.Popen(['python3', '../scripts/icatagent', 
                            '--inbound-transport', 'http', '0.0.0.0', '8000', 
                            '--inbound-transport', 'http', '0.0.0.0', '8001', 
                            '--inbound-transport', 'ws', '0.0.0.0', '8002',
                            '--outbound-transport', 'ws', 
                            '--outbound-transport', 'http', 
                            '--genesis-transactions', genesis,
                            '--seed', 'my_seed_000000000000000000000666',
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
        resp = urllib.request.urlopen('http://localhost:8080/api/docs/swagger.json')
        p = resp.read()
        assert b'Indy Catalyst Agent' in p

        # get an invitation
        headers = {"accept": "application/json"}
        req = urllib.request.Request('http://localhost:8080/connections/create-invitation', headers=headers, method='POST')
        resp = urllib.request.urlopen(req)
        p = resp.read()
        print(p)

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

        credential_definition_body = {"schema_id": schema_id}
        credential_definition_response = requests.post(
            f"http://localhost:8080/credential-definitions", json=credential_definition_body
        )
        credential_definition_response_body = credential_definition_response.json()
        credential_definition_id = credential_definition_response_body[
            "credential_definition_id"
        ]

        print(f"cred def id: {credential_definition_id}")

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
