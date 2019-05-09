import subprocess
import time
import urllib.request, urllib.parse
import threading
import os
import requests
import random
import sys


# web.py to run a service for webhook callbacks from the agent
import web

from threading import Lock

s_print_lock = Lock()


urls = (
  '/webhooks/topic/(.*)/', 'webhooks'
)


def output_reader(proc):
    for line in iter(proc.stdout.readline, b''):
        #print('got line: {0}'.format(line.decode('utf-8')), end='')
        pass


def stderr_reader(proc):
    for line in iter(proc.stderr.readline, b''):
        #print('got line: {0}'.format(line.decode('utf-8')), end='')
        pass


def s_print(*a, **b):
    """Thread safe print function"""
    with s_print_lock:
        print(*a, **b)


# agent webhook callbacks
class webhooks:
    def GET(self, topic):
        s_print("GET: topic=", topic)
        return ""

    def POST(self, topic):
        data = web.data() # you can get data use this method
        s_print("Callback: topic=", topic, ", data=", data)
        return ""


def background_hook_service():
    # run app and respond to agent webhook callbacks (run in background)
    app = web.application(urls, globals())
    app.run()  


def main():
    my_env = os.environ.copy()
    my_env["PYTHONPATH"] = ".."

    # start and expose a REST callback service
    webhook_port = int(sys.argv[1])
    my_env["WEBHOOK_URL"] = "http://localhost:" + str(webhook_port) + "/"

    # TODO genesis transactions from file or url
    with open('local-genesis.txt', 'r') as genesis_file:
        genesis = genesis_file.read()
    #print(genesis)

    # TODO seed from input parameter; optionally register the DID
    rand_name = str(random.randint(100000, 999999))
    seed = ('my_seed_000000000000000000000000' + rand_name)[-32:]
    alias = 'Alice Agent'
    register_did = False # Alice doesn't need to register her did
    if register_did:
        print("Registering", alias, "with seed", seed)
        ledger_url = 'http://localhost:9000'
        headers = {"accept": "application/json"}
        data = {"alias": alias, "seed": seed, "role": "TRUST_ANCHOR"}
        resp = requests.post(ledger_url+'/register', json=data)
        nym_info = resp.text
        print(nym_info)

    # start agent sub-process
    in_port_1  = webhook_port + 1
    in_port_2  = webhook_port + 2
    in_port_3  = webhook_port + 3
    admin_port = webhook_port + 4
    admin_url  = 'http://localhost:' + str(admin_port)
    agent_proc = subprocess.Popen(['python3', '../scripts/icatagent', 
                            '--inbound-transport', 'http', '0.0.0.0', str(in_port_1), 
                            '--inbound-transport', 'http', '0.0.0.0', str(in_port_2), 
                            '--inbound-transport', 'ws', '0.0.0.0', str(in_port_3),
                            '--outbound-transport', 'ws', 
                            '--outbound-transport', 'http', 
                            '--genesis-transactions', genesis,
                            '--wallet-type', 'indy',
                            '--wallet-name', 'alice'+rand_name,
                            '--wallet-key', 'alice'+rand_name,
                            '--seed', seed,
                            '--admin', '0.0.0.0', str(admin_port)],
                            stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE,
                            env=my_env)
    time.sleep(0.5)
    t1 = threading.Thread(target=output_reader, args=(agent_proc,))
    t1.start()
    t2 = threading.Thread(target=stderr_reader, args=(agent_proc,))
    t2.start()
    time.sleep(3.0)
    print("Admin url is at:", admin_url)
    try:
        time.sleep(0.2)

        # check swagger content
        resp = requests.get(admin_url+'/api/docs/swagger.json')
        p = resp.text
        assert 'Indy Catalyst Agent' in p

        # run app and respond to agent webhook callbacks (run in background)
        webhook_thread = threading.Thread(target=background_hook_service)
        webhook_thread.daemon = True
        webhook_thread.start()

        print("Stuff is running!")

        # respond to an invitation
        print("#9 Input faber.py invitation details")
        details = input('invite details: ')
        resp = requests.post(admin_url+'/connections/receive-invitation', json=details)
        p = resp.text
        print(p)

        val = input("<Enter> to Exit :-D") 

    except Exception as e:
        print(e)
    finally:
        time.sleep(2.0)
        agent_proc.terminate()
        try:
            agent_proc.wait(timeout=0.5)
            print('== subprocess exited with rc =', agent_proc.returncode)
        except subprocess.TimeoutExpired:
            print('subprocess did not terminate in time')
        sys.exit()

if __name__ == "__main__":
    main()
