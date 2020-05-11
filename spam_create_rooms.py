import asyncio
import json
import os
import random
import re
import requests
import subprocess
import string
import sys
from concurrent.futures import ThreadPoolExecutor
try:
    from io import BytesIO
except ImportError:
    from StringIO import StringIO as BytesIO


def randomString(stringLength=8):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


def create_rooms(stoken, rtoken):
    # Create 10 000 rooms and invite the user receiver
    f = open('/root/rooms.txt', 'w+')
    for i in range(10000):
        # Create room
        url = 'http://localhost:8008/_matrix/client/r0/createRoom?access_token='  + stoken
        data = json.dumps({"room_alias_name": randomString(25)})
        r = requests.post(url, data=data)
        room_id = r.json()['room_id']
        f.write(room_id + '\n')

        # Invite receiver
        url = 'http://localhost:8008/_matrix/client/r0/rooms/' + room_id + '/invite?access_token='  + stoken
        data = json.dumps({'user_id': '@receiver:tenbillions.twily.me'})
        r = requests.post(url, data=data)

        # Join as receiver
        url = 'http://localhost:8008/_matrix/client/r0/rooms/' + room_id + '/join?access_token='  + rtoken
        data = json.dumps({})
        r = requests.post(url, data=data)
    f.close()


async def get_data_asynchronous(stoken, rtoken):
    with ThreadPoolExecutor(max_workers=10) as executor:
        # Set any session parameters here before calling `fetch`
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                create_rooms,
                stoken,
                rtoken,
            )
        ]
        for response in await asyncio.gather(*tasks):
            if response:
                pass


def main():
    stoken = ''
    rtoken = ''
    create_rooms(stoken, rtoken)

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(get_data_asynchronous(stoken, rtoken))
    loop.run_until_complete(future)


try:
    main()
except KeyboardInterrupt:
    exit(0)
