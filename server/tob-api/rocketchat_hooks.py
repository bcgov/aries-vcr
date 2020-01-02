from os import environ
import asyncio
import aiohttp

import time
import datetime

import json

LOG_LEVELS = {
    '0': 'ERROR',
    '1': 'WARNING',
    '2': 'INFO'
}

log_level = environ.get('WEBHOOK_LEVEL', '0')
if log_level > '2':
    log_level = '2'
elif log_level < '0':
    log_level = '0'

webhook_url = environ.get('WEBHOOK_URL', '')


def get_webhook_payload(level, message):
    project_name = environ.get('PROJECT_NAME', "von-bc-registries-agent")
    friendly_project_name = environ.get('FRIENDLY_PROJECT_NAME', "BC Registries")
    payload = {
        "friendlyProjectName": friendly_project_name,
        "projectName": project_name,
        "statusCode": LOG_LEVELS[level],
        "message": message
    }
    return payload

async def _post_url(the_url, payload):
    async with aiohttp.ClientSession() as session:
        headers = {'Content-Type': 'application/json'}
        async with session.post(the_url, json=payload, headers=headers) as resp:
            r_status = resp.status
            r_text = await resp.text()
            return (r_status, r_text)

async def post_msg_to_webhook(level, message):
    if webhook_url and 0 < len(webhook_url):
        if level and level <= log_level:
            payload = get_webhook_payload(level, message)
            (status, text) = await _post_url(webhook_url, payload)


async def log_info(message):
   await post_msg_to_webhook('2', message)


async def log_warning(message):
    await post_msg_to_webhook('1', message)


async def log_error(message):
    await post_msg_to_webhook('0', message)