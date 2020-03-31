users_file_name = 'create_matrix_users.txt' # Need to be placed in the same directory as this script
username_domain = 'example.com' # The domain in your usernames
homeserver = 'matrix.example.com' # Your homeserver fqdn. Might be different that the usernames
workers = 100 # How many curl's to do at once
# Admin Access token
bearer_token = 'ohbiug3haikai1Pheove2Neich3ogheicaiD3ciengailee9thohmeiFah2oogoceepohP5rieb5chohc5queec6cifeiChohpe7kie0Ahshai1vai9xea3eeroo2Aegheiquei9iel3ooshik7iolei4Ohxaivahre5hohJoonie6pooquohhooqu4eeZah2Aang2eo7ohy5jiemaip5Hie4yi9Queehev6su8mo2ukae9phu0eefaiwaub1Thoo8heepie5teevei9yah5IuseifoafiquieZ9oht'
password = 'Password123' # The password to set for all users


# Import stuff
import json
import os
import random
import re
import requests
import subprocess
import sys
import asyncio
from concurrent.futures import ThreadPoolExecutor
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


# Set paths
workDir = os.path.dirname(os.path.realpath(__file__))
users_file_path = open(os.path.join(workDir, users_file_name))


# Read users file
users = [line for line in users_file_path]
# random.shuffle(users)


def curl(line):
    '''
    Do curl stuff.

    Args:
        line: a text string

    Returns
        json response
    '''
    user = str(line).strip()

    url = 'https://' + homeserver + '/_synapse/admin/v2/users/@' + user + ':' + username_domain
    x = 'Bearer ' + bearer_token
    headers = {'Authorization': x, 'Content-Type': 'application/json'}
    data = json.dumps({'password': password})
    r = requests.put(url, headers=headers, data=data)
    
    return(r.json())


async def get_data_asynchronous():
    with ThreadPoolExecutor(max_workers=workers) as executor:
        # Set any session parameters here before calling `fetch`
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                curl,
                line,
            )
            for line in users
        ]
        for response in await asyncio.gather(*tasks):
            if response:
                print(response)


def main():
    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous())
    loop.run_until_complete(future)

main()