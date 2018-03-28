#! /usr/local/bin/python3

#
# "requests" must be installed - pip3 install requests
#

import argparse
import json
import os
import sys
from glob import glob
from os.path import dirname, join
import threading
import time
import requests
from requests.auth import HTTPBasicAuth

import string
from random import *


parser = argparse.ArgumentParser(description='A TheOrgBook Claim loader.  Supports randomization for test data and threading for fast loading')
parser.add_argument('--random', action='store_true', required=False,
                    help='If data is to be randomized before loading (useful for test data)')
parser.add_argument('--proofs', action='store_true', required=False,
                    help='If calculate proofs as claims are loaded')
parser.add_argument('--env', metavar='env', type=str, default='local',
                    help='Permitify and TheOrgBook services are on local/dev/test host')
parser.add_argument('--inputdir', metavar='inputdir', type=str, default="Claims",
                    help='The directory containing JSON claims to be loaded')
parser.add_argument('--threads', metavar='threads', type=int, default=1,
                    help='The number of threads to run for concurrent loading')
parser.add_argument('--loops', metavar='loops', type=int, default=1,
                    help='The number of times to loop through the list')

args = parser.parse_args()

print('Environment = \'%s\'' % args.env)
if os.path.exists(args.inputdir):
    print('Processing input directory \'%s\'' % args.inputdir)
else:
    print('Directory not found \'%s\'' % args.inputdir)

print('Threads = {}'.format(args.threads))

if args.random or args.threads > 1 or args.loops > 1:
    print('Randomizing!')
else:
    print('NOT Randomizing.')

loop_locks = {
    'Reg': threading.Semaphore(),
    'Worksafe': threading.Semaphore(),
    'Finance': threading.Semaphore(),
    'Health': threading.Semaphore(),
    'City': threading.Semaphore(),
    'Liquor': threading.Semaphore()
}

URLS = {
  'local': {
        # bc_registries (needs to be first)
        'Reg': 'http://localhost:5000',
        # worksafe_bc
        'Worksafe': 'http://localhost:5001',
        # ministry_of_finance
        'Finance': 'http://localhost:5002',
        # fraser_valley_health_authority
        'Health': 'http://localhost:5003',
        # city_of_surrey
        'City': 'http://localhost:5004',
        # liquor_control_and_licensing_branch
        'Liquor': 'http://localhost:5005'
    },
  'dev': {
        # bc_registries (needs to be first)
        'Reg': 'https://bc-registries-devex-von-permitify-dev.pathfinder.gov.bc.ca',
        # worksafe_bc
        'Worksafe': 'https://worksafe-bc-devex-von-permitify-dev.pathfinder.gov.bc.ca',
        # ministry_of_finance
        'Finance': 'https://ministry-of-finance-devex-von-permitify-dev.pathfinder.gov.bc.ca',
        # fraser_valley_health_authority
        'Health': 'https://fraser-valley-health-authority-devex-von-permitify-dev.pathfinder.gov.bc.ca',
        # city_of_surrey
        'City': 'https://city-of-surrey-devex-von-permitify-dev.pathfinder.gov.bc.ca',
        # liquor_control_and_licensing_branch
        'Liquor': 'https://liquor-control-and-licensing-branch-devex-von-permitify-dev.pathfinder.gov.bc.ca'
    },
  'test': {
        # bc_registries (needs to be first)
        'Reg': 'https://bc-registries-devex-von-permitify-test.pathfinder.gov.bc.ca',
        # worksafe_bc
        'Worksafe': 'https://worksafe-bc-devex-von-permitify-test.pathfinder.gov.bc.ca',
        # ministry_of_finance
        'Finance': 'https://ministry-of-finance-devex-von-permitify-test.pathfinder.gov.bc.ca',
        # fraser_valley_health_authority
        'Health': 'https://fraser-valley-health-authority-devex-von-permitify-test.pathfinder.gov.bc.ca',
        # city_of_surrey
        'City': 'https://city-of-surrey-devex-von-permitify-test.pathfinder.gov.bc.ca',
        # liquor_control_and_licensing_branch
        'Liquor': 'https://liquor-control-and-licensing-branch-devex-von-permitify-test.pathfinder.gov.bc.ca'
    },
    'wallet': {
        # if we're just dumping data into the wallet it all goes into the same url
        'Reg': 'http://localhost:8000/api/v1/keyval/',
        'Worksafe': 'http://localhost:8000/api/v1/keyval/',
        'Finance': 'http://localhost:8000/api/v1/keyval/',
        'Health': 'http://localhost:8000/api/v1/keyval/',
        'City': 'http://localhost:8000/api/v1/keyval/',
        'Liquor': 'http://localhost:8000/api/v1/keyval/'
    }
}

this_dir = dirname(__file__)

claim_files = glob(join(this_dir, args.inputdir, 'Claims_*'))

do_it_random = (args.random or args.threads > 1 or args.loops > 1)
num_loops = args.loops
use_env = args.env

min_char = 8
max_char = 12
allchar = "0123456789abcdef"

# generate a short random string
def random_string(i):
    r_str = "-" + str(i) + "-" + "".join(choice(allchar) for x in range(randint(min_char, max_char)))
    return r_str

# check if field is a candidate for randomization
def should_we_randomify(key, value):
    # if value is all numeric, don't randomize
    if value.isdigit():
        return False

    # key like "schema" don't randomize
    if "schema" in key.lower():
        return False;

    # key like "type" probably a pick-list
    if "_type" in key.lower():
        return False;

    # boolean flags
    if value == "True" or value == "False":
        return False;

    # postal code or province
    if key.lower() == "city" or key.lower() == "province" or key.lower() == "postal_code" or key.lower() == "country":
        return False

    # one more!
    if key.lower() == "coverage_description":
        return False

    # ok go for it!
    return True

# randomize our test data so we can re-use it
def randomify(claim, i):
    for key in claim:
        if should_we_randomify(key, claim[key]):
            claim[key] = claim[key] + random_string(i)
    return claim

class myThread (threading.Thread):
   def __init__(self, threadID, name, counter):
      threading.Thread.__init__(self)
      self.threadID = threadID
      self.name = name
      self.counter = counter
   def run(self):
      print("Starting " + self.name)
      main_load(use_env, do_it_random, num_loops, self.counter)
      print("Exiting " + self.name)

def main_load(env, do_it_random, num_loops, thread_id):
    # login to wallet
    if env == 'wallet':
        try:
            my_url = "http://localhost:8000/api/v1/api-token-auth/"
            response = requests.post(my_url, data = {"username":"wall-e", "password":"pass1234"})
            json_data = response.json()
            remote_token = 'Token ' + json_data["token"]
            print("Authenticated remote wallet server: " + remote_token)
        except:
            raise Exception(
                'Could not login to wallet. '
                'Is the Wallet Service running?')

    # Create new threads
    loop_start_time = time.time()
    loop_claims = 0
    claim_elapsed_time = 0
    proof_elapsed_time = 0
    for _ in range(0, num_loops):
        # Each filename is a full permitify recipe
        for filename in claim_files:
            with open(filename, 'r') as file:
                print('==============================================')
                print('FileName: {}'.format(filename))
                content = file.read()
                permitify_services = json.loads(content)
                legal_entity_id = None
                for service_name in URLS[env]:
                    if service_name not in permitify_services:
                        continue
                    for claim in permitify_services[service_name]:
                        if do_it_random:
                            claim = randomify(claim, thread_id)

                        if service_name != 'Reg':
                            claim['legal_entity_id'] = legal_entity_id
                            print('\n\n')
                            print('Issuing permit: {}'.format(
                                claim['schema']
                            ))
                        else:
                            print('\n\n')
                            print('==============================================')
                            print('Registering new business: {}'.format(
                                claim['legal_name']
                            ))
                            print('==============================================')

                        claim['address_line_2'] = ""

                        print('\n\nSubmitting Claim:\n\n{}'.format(claim))

                        if env == 'wallet':
                            legal_entity_id = "da0" + random_string(thread_id) + random_string(thread_id) + random_string(thread_id)
                            claim['legal_entity_id'] = legal_entity_id
                            wallet_item = {
                                # 'wallet_name':legal_entity_id,
                                'wallet_name':'TheOrgBook_Holder_Wallet::' + legal_entity_id,
                                'item_type':'claim',
                                'item_id':legal_entity_id,
                                'item_value':json.dumps(claim)
                            }
                            print(json.dumps(wallet_item))
                            # post to the wallet service
                            try:
                                response = requests.post(
                                    '{}'.format(
                                        URLS[env][service_name]),
                                    headers={'Authorization': remote_token},
                                    json=wallet_item
                                )
                                result_json = response.json()
                            except:
                                raise Exception(
                                    'Could not submit claim. '
                                    'Is the Wallet Service running?')
                        else:
                            try:
                                start_time = time.time()
                                loop_locks[service_name].acquire()
                                response = requests.post(
                                    '{}/submit_claim'.format(
                                        URLS[env][service_name]),
                                    json=claim
                                )
                                loop_locks[service_name].release()
                                result_json = response.json()
                                elapsed_time = time.time() - start_time
                                claim_elapsed_time = claim_elapsed_time + elapsed_time
                                print('Claim elapsed time >>> {}'.format(elapsed_time))
                            except:
                                loop_locks[service_name].release()
                                raise Exception(
                                    'Could not submit claim. '
                                    'Are Permitify and Docker running?')
                            print('\n\n Response from permitify:\n\n{}'.format(result_json))
                            if service_name == 'Reg':
                                legal_entity_id = result_json['result']['orgId']
                        loop_claims = loop_claims + 1

                        if args.proofs:
                            # "submit_claim" returns the id of the org, not the claim, so fake it pick any random claim
                            my_id = randint(1, 6*(result_json['result']['id']-1))
                            print('\n\nRequesting Proof:\n\n{}'.format(my_id))
                            try:
                                start_time = time.time()
                                response = requests.get(
                                    '{}/{}/verify'.format(
                                        "http://localhost:8081/api/v1/verifiableclaims", str(my_id))
                                )
                                elapsed_time = time.time() - start_time
                                proof_elapsed_time = proof_elapsed_time + elapsed_time
                                print('Proof elapsed time >>> {}'.format(elapsed_time))
                                result_json = response.json()
                            except:
                                raise Exception(
                                    'Could not submit proof request. '
                                    'Are Permitify and Docker running?')
                            print('\n\n Response from TOB:\n\n')

    print('Claim elapsed time >>> {}, {} claims'.format(claim_elapsed_time, loop_claims))
    if args.proofs:
        print('Proof elapsed time >>> {}, {} claims'.format(proof_elapsed_time, loop_claims))

if __name__ == '__main__':
    try:
        URLS[use_env]
    except KeyError:
        print('{} --env <local|dev|test>'.format(sys.argv[0]))
    else:
        execution_start = time.time()
        my_threads = []
        for i in range(0, args.threads):
            thread = myThread(i, "Thread-{}".format(i), i)
            # Start new Threads
            thread.start()
            my_threads.append(thread)
            time.sleep(1)
        for i in range(0, args.threads):
            my_threads[i].join()
        execution_elapsed = time.time() - execution_start
        print("Exiting Main Thread, time = {} secs".format(execution_elapsed))

