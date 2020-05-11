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


def send_message(token,room):
    # Send a message to the room
    room = room.replace('!', '%21').strip()
    url = 'http://localhost:8008/_matrix/client/r0/rooms/' + room + '/send/m.room.message?access_token=' + token
    data = json.dumps({'body': '@receiver:tenbillions.twily.me ' + randomString(random.randint(1,15)), 'msgtype': 'm.text'})
    requests.post(url, data=data)


async def get_data_asynchronous(token, rooms):
    with ThreadPoolExecutor(max_workers=20) as executor:
        # Set any session parameters here before calling `fetch`
        loop = asyncio.get_event_loop()
        tasks = [
            loop.run_in_executor(
                executor,
                send_message,
                token,
                room,
            )
            for room in rooms
        ]
        for response in await asyncio.gather(*tasks):
            if response:
                pass


def main():
    stoken = ''

    while True:
        rooms = [line for line in open('/root/rooms.txt', 'r')]

        loop = asyncio.get_event_loop()
        future = asyncio.ensure_future(get_data_asynchronous(stoken, rooms))
        loop.run_until_complete(future)


try:
    main()
except KeyboardInterrupt:
    exit(0)
