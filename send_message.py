# Config
homeserver_url = "matrix.example.com"
access_token = ""


# # Import modules
import json
import requests
import sys

if __name__ == "__main__":
    room_id = sys.argv[1].replace("!", "%21").strip()
    url = "https://%s/_matrix/client/r0/rooms/%s/send/m.room.message" %(homeserver_url, room_id)
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json"
    }
    data = {
        "msgtype": "m.text",
        "body": sys.argv[2]
    }
    requests.post(
        url=url,
        headers=headers,
        data=json.dumps(data)
    )
