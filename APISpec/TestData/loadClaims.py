#!/usr/bin/env python3
#
# Copyright 2017-2018 Government of Canada
# Public Services and Procurement Canada - buyandsell.gc.ca
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


import asyncio
import argparse
import json
import os
import time

import aiohttp

DEFAULT_AGENT_URL = os.environ.get("AGENT_URL", "http://localhost:5000/bcreg")

parser = argparse.ArgumentParser(
    description="Issue one or more credentials via von-x"
)
parser.add_argument(
    "dir", default="v2_creds", help="the path to a credential directory"
)
parser.add_argument(
    "-u",
    "--url",
    default=DEFAULT_AGENT_URL,
    help="the URL of the von-x service",
)
parser.add_argument(
    "-p",
    "--parallel",
    action="store_true",
    help="submit the credentials in parallel",
)

args = parser.parse_args()

AGENT_URL = args.url
DATA_DIR = args.dir
PARALLEL = args.parallel


def get_dir_dirs(dir_path):
    try:
        return next(os.walk(dir_path))[1]
    except StopIteration:
        return []


def get_dir_files(dir_path):
    try:
        return next(os.walk(dir_path))[2]
    except StopIteration:
        return []


async def issue_cred(
    http_client, cred_path, schema_name, schema_version, ident
):
    try:
        with open(cred_path) as cred_file:
            cred = json.load(cred_file)
    except json.decoder.JSONDecodeError:
        print("Credential could not be parsed, skipping")
        return

    # Shim to accept single item array from test data output
    if type(cred) is list:
        cred = cred[0]

    print("Submitting credential {} {}".format(ident, cred_path))

    start = time.time()
    try:
        response = await http_client.post(
            "{}/issue-credential".format(AGENT_URL),
            params={"schema": schema_name, "version": schema_version},
            json=cred,
        )
        if response.status != 200:
            raise RuntimeError(
                "Credential could not be processed: {}".format(
                    await response.text()
                )
            )
        result_json = await response.json()
    except Exception as exc:
        raise Exception(
            "Could not issue credential. " "Are von-x and TheOrgBook running?"
        ) from exc

    elapsed = time.time() - start
    print(
        "Response to {} from von-x ({:.2f}s):\n\n{}\n".format(
            ident, elapsed, result_json
        )
    )


async def submit_all(data_dir, parallel=True):
    schema_type_paths = get_dir_dirs(data_dir)
    start = time.time()

    all = []
    idx = 1

    for schema_type_path in schema_type_paths:

        # We expect path convention <schema_name>::<schema_version>
        schema_name = schema_type_path.split("::")[0]
        schema_version = schema_type_path.split("::")[1]

        cred_paths = get_dir_files("{}/{}".format(data_dir, schema_type_path))

        async with aiohttp.ClientSession() as http_client:

            for cred_path in cred_paths:
                req = issue_cred(
                    http_client,
                    "{}/{}/{}".format(data_dir, schema_type_path, cred_path),
                    schema_name,
                    schema_version,
                    idx,
                )
                if parallel:
                    all.append(req)
                else:
                    await req
                idx += 1

            if all:
                await asyncio.gather(*all)

    elapsed = time.time() - start
    print("Total time: {:.2f}s".format(elapsed))


asyncio.get_event_loop().run_until_complete(submit_all(DATA_DIR, PARALLEL))
