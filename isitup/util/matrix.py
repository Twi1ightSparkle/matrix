# Import modules
import json
import requests
from datetime import datetime


def send_message(homeserver, room, token, message=None):
    """Send a message to a room

    Args:
        homeserver: Full url to delegated hostname. Incl port is required. Ex: https://matrix.example.com
        room: A matrix room ID
        token: Access token for user
        message: Optional message to send. Defaults to current timestamp

    Returns:
        None if successful, otherwise an error
    """

    if not message:
        message = datetime.fromtimestamp(datetime.utcnow())

    room = room.replace('!', '%21').strip()
    url = f'{homeserver.strip()}/_matrix/client/r0/rooms/{room}/send/m.room.message?access_token={token.strip()}'
    data = json.dumps({'body': message, 'msgtype': 'm.text'})
    try:
        response = requests.post(url, data=data).json()
    except Exception as e:
        return(e)
    
    if response['event']:
        return(None)
    else:
        return(response['errorcode'])
