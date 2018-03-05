#! /usr/local/bin/python3

#
# "requests" must be installed - pip3 install requests
#

import json
import os
import sys
from glob import glob
from os.path import dirname, join

import requests

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
    }
}

this_dir = dirname(__file__)

claim_files = glob(join(this_dir, 'Claims', 'Claims_*'))


def main(env):
    # Each filename is a full permitify recipe
    for filename in claim_files:
        with open(filename, 'r') as file:
            content = file.read()
            permitify_services = json.loads(content)
            legal_entity_id = None
            for service_name in URLS[env]:
                if service_name not in permitify_services:
                    continue
                for claim in permitify_services[service_name]:
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

                    try:
                        response = requests.post(
                            '{}/submit_claim'.format(
                                URLS[env][service_name]),
                            json=claim
                        )
                        result_json = response.json()
                    except:
                        raise Exception(
                            'Could not submit claim. '
                            'Are Permitify and Docker running?')

                    print('\n\n Response from permitify:\n\n{}'.format(result_json))

                    if service_name == 'Reg':
                        legal_entity_id = result_json['result']['orgId']


if __name__ == '__main__':
    if len(sys.argv) < 2:
        print('{} {{local|dev|test}}'.format(sys.argv[0]))
    else:
        try:
            URLS[sys.argv[1]]
        except KeyError:
            print('{} {{local|dev|test}}'.format(sys.argv[0]))
        else:
            env = sys.argv[1]
            main(env)
