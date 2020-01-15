#!/usr/bin/env python3
#
# Copyright 2019 Province of British Columbia
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#


import argparse
import asyncio
import json
import os
import time

import aiohttp

RECEIVE_CREDENTIAL_URL = os.environ.get(
    "RECEIVE_CREDENTIAL_URL", "http://localhost:8080/agentcb/debug/receive-credential/"
)

parser = argparse.ArgumentParser(
    description="Store credentials in the Credential Registry without using an agent"
)
parser.add_argument("paths", nargs="+", help="the path to a credential JSON file")
parser.add_argument(
    "-u",
    "--url",
    default=RECEIVE_CREDENTIAL_URL,
    help="the URL of the /receive-credential endpoint",
)
parser.add_argument(
    "-p", "--parallel", action="store_true", help="submit the credentials in parallel"
)

args = parser.parse_args()

REGISTRY_URL = args.url
CRED_PATHS = args.paths
PARALLEL = args.parallel


async def issue_cred(http_client, cred_path, ident):
    with open(cred_path) as cred_file:
        cred_list = json.load(cred_file)

    # Handle everything as a list
    if type(cred_list) is not list:
        cred = cred_list
        cred_list = []
        cred_list.append(cred)

    for cred in cred_list:

        raw_cred = cred["raw_credential"]

        if not raw_cred:
            raise ValueError("Credential could not be parsed")
        schema_id = raw_cred.get("schema_id")
        if not schema_id:
            raise ValueError("No schema_id defined")
        cred_def_id = raw_cred.get("cred_def_id")
        if not cred_def_id:
            raise ValueError("No cred_def_id defined")
        values = raw_cred.get("schema_id")
        if not values:
            raise ValueError("No attribute values defined")

        print("Submitting credential {} {}".format(ident, cred))

        start = time.time()
        try:
            response = await http_client.post(REGISTRY_URL, json=cred)
            if response.status != 200:
                raise RuntimeError(
                    "Credential could not be processed: {}".format(
                        await response.text()
                    )
                )
            result_json = await response.json()
        except Exception as exc:
            raise Exception(
                "Could not issue credential. Is the Credential Registry running?"
            ) from exc

        elapsed = time.time() - start
        print(
            "Response to {} from Credential Registry ({:.2f}s):\n\n{}\n".format(
                ident, elapsed, result_json
            )
        )


async def submit_all(cred_paths, parallel=True):
    start = time.time()
    async with aiohttp.ClientSession() as http_client:
        all = []
        idx = 1
        for cred_path in cred_paths:
            req = issue_cred(http_client, cred_path, idx)
            if parallel:
                all.append(req)
            else:
                await req
            idx += 1
        if all:
            await asyncio.gather(*all)
    elapsed = time.time() - start
    print("Total time: {:.2f}s".format(elapsed))


asyncio.get_event_loop().run_until_complete(submit_all(CRED_PATHS, PARALLEL))
