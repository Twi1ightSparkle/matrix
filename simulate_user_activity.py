users_file_name = 'simulate_user_activity.txt' # Need to be placed in the same directory as this script
username_domain = 'tey-staging.modular.im' # The domain in your usernames
homeserver = 'tey-staging.modular.im' # Your homeserver fqdn. Might be different that the usernames
room = '!DNhBNbJHedlbHTGBpA' # Room id of a public room on the homeserver anyone can join
workers = 5 # How many curl's to do at once


# Import stuff
import asyncio
import json
import os
import random
import re
import requests
import subprocess
import sys
import time
from concurrent.futures import ThreadPoolExecutor
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


# Set paths
workDir = os.path.dirname(os.path.realpath(__file__))
users_file_path = open(os.path.join(workDir, users_file_name))
token_file = os.path.splitext(users_file_name)[0]
if os.path.isfile(os.path.join(workDir, token_file + '_tokens.txt')):
    


# Read users file
users = [line for line in users_file_path]
random.shuffle(users)
users_file_path.close()
token_file_path.close()


def curl(line):
    '''
    Do curl stuff.

    Args:
        line: a text string
    '''
    user,password = str(line).strip().split(':')

    if not user and not password:
        return(False)
        
    # Get token
    url = 'https://' + homeserver + '/_matrix/client/r0/login'
    data = json.dumps({'type': 'm.login.password', 'user': user, 'password': password})
    r = requests.post(url, data=data)

    while r.json()['errcode']:
        if r.json()['errcode'] == 'M_FORBIDDEN':
            return('M_FORBIDDEN error for user ' + user)
        if r.json()['errcode'] == 'M_LIMIT_EXCEEDED':
            time.sleep((r.json()['retry_after_ms'] / 1000) + 1)
            r = requests.post(url, data=data)
    
    try:
        token = r.json()['access_token']
    except KeyError as e:
        return(e, 'access_token error for user ' + user)


    # Join room
    url = 'https://' + homeserver + '/_matrix/client/r0/join/' + room + ':' + username_domain + '?access_token=' + token
    r = requests.post(url)

    # If terms and conditions are not yet agreed to for this user
    if r.json()['errcode'] == 'M_CONSENT_NOT_GIVEN':
        consent_uri = r.json()['consent_uri']
        h = consent_uri.rsplit('=', 1)[-1]
        data_accept = 'v=1.0&u=' + user + '&h=' + h
        url_accept = 'https://' + homeserver + '/_matrix/consent?' + data_accept
        requests.post(url_accept)

        # Join room
        requests.post(url)

    # Send a message to the room
    url = 'https://' + homeserver + '/_matrix/client/r0/rooms/' + room + ':' + username_domain +'/send/m.room.message/m.' + str(int(time.time())) + '?access_token=' + token
    message = 'Hi everyone from ' + user
    data = json.dumps({'body': message, 'msgtype': 'm.text'})
    r = requests.put(url, data=data)
    

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