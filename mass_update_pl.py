# Config
homeserver_delegated_url = "https://matrix.example.com"
homeserver_url = "example.com"

# Datbase config
server = "127.0.0.1"
port = 5431
database = "synapse"
username = "synapse"
password = "V3ryS3cret"

# User to make change with, this user should be admin in all rooms returned by rooms_query
admin_user = "@alice:example.comm"
admin_token = "MDAxxxxxx"

# User to promote in the rooms
promote_user = "@bob:example.com"

# Set power level for promote_user = admin_user - minus_pl
# Must be 0 or higher
# If this is 0, you will not be able to undo the change
minus_pl = 1

# PostgreSQL query to get rooms to work with. Must return room_alias in column 0 and room_id in column 1
rooms_query = """
    SELECT
        room_aliases.room_alias,
        rooms.room_id
    FROM
        rooms
        LEFT JOIN room_aliases ON rooms.room_id = room_aliases.room_id
    WHERE
        rooms.room_id = '!lkFcylzZFTWNDWlcjs:example.com'
"""


# Import modules
from datetime import datetime
import json
import os
import progressbar
import psycopg2
import requests


# Log to this file. Default is result.csv in the same directory as this script file
log_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "result.csv")


def log_writer(room_id, room_alias, status, status_code, target, change_user, old_pl, new_pl, content):
    """Write timestamp and message to logfile"""
    time_stamp = datetime.utcnow()
    time_stamp_short = time_stamp.strftime("%Y.%m.%dT%H.%M.%S.%fZ")

    if os.path.isfile(log_file_path):
        csv_header = False
    else:
        csv_header = True

    log = open(log_file_path, "a+")

    if csv_header:
        log.write("time_stamp;room_id;room_alias;status;status_code;target;change_user;old_pl;new_pl;content\n")
    log.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (
        str(time_stamp_short),
        str(room_id),
        str(room_alias),
        str(status),
        str(status_code),
        str(target),
        str(change_user),
        str(old_pl),
        str(new_pl),
        str(content)
    ))
    log.close()


def clean_log_text(input_string):
    "Removes newlines, semi colons and double quotes to make line work with CSV log file"
    return str(input_string).replace("\n", "").replace(";", ":").replace("\"", "'")



if __name__ == "__main__":

    # Connect to database
    connection = psycopg2.connect(user=username, password=password, host=server, port=port, database=database, connect_timeout=3)
    cursor = connection.cursor()

    # Get list of rooms. Creates a list: [[room_alias, room_id], ...]
    rooms = []
    cursor.execute(rooms_query)
    mobile_records = cursor.fetchall() 
    for row in mobile_records:
        rooms.append(row)


    # Log new operation
    log_writer(
        room_id=None,
        room_alias=None,
        status="new_operation",
        status_code=None,
        target=None,
        change_user=None,
        old_pl=None,
        new_pl=None,
        content="New operation started. %s rooms to change" % len(rooms)
    )


    # Loop over the rooms
    pbar = progressbar.ProgressBar(maxval=len(rooms)).start()
    for room in pbar(rooms):

        # Request URL and headers
        target = homeserver_delegated_url + "/_matrix/client/r0/rooms/" + room[1] + "/state/m.room.power_levels"
        headers = {
            "Authorization": "Bearer %s" % admin_token,
            "Content-Type": "application/json"
        }


        # Get current m.room.power_levels
        power_levels = requests.request(
            method="GET",
            url=target,
            headers=headers
        )


        # If error on GET, log it and move on to next room
        if not power_levels.status_code == 200:
            try:
                content = clean_log_text(power_levels.json())
            except json.decoder.JSONDecodeError:
                content = clean_log_text(power_levels.content)
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="get_error",
                status_code=power_levels.status_code,
                target=target,
                change_user=promote_user,
                old_pl=None,
                new_pl=None,
                content=content
            )
            continue


        # Get the power_levels state event from requests data
        power_levels = power_levels.json()


        # Get current PL for promote_user or default to 0 if it does not have any in the room
        try:
            old_pl = power_levels["users"][promote_user]
        except KeyError:
            old_pl = 0


        # Get PL for admin_user and append promote_user to state event
        admin_current_pl = power_levels["users"][admin_user]
        new_pl = admin_current_pl - minus_pl
        power_levels["users"][promote_user] = new_pl


        # Log and move on to next room if no change will be made
        if old_pl == new_pl:
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="unchanged",
                status_code=None,
                target=None,
                change_user=promote_user,
                old_pl=old_pl,
                new_pl=None,
                content=None
            )
            continue


        # Send new state event to the room
        update_status = requests.request(
            method="PUT",
            url=target,
            headers=headers,
            data=json.dumps(power_levels)
        )


        # If error on PUT, log it and move on to next room
        if not update_status.status_code == 200:
            try:
                content = clean_log_text(update_status.json())
            except json.decoder.JSONDecodeError:
                content = clean_log_text(update_status.content)
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="put_error",
                status_code=update_status.status_code,
                target=target,
                change_user=promote_user,
                old_pl=None,
                new_pl=None,
                content=content
            )
            continue


        # Log success
        try:
            content = clean_log_text(update_status.json())
        except json.decoder.JSONDecodeError:
            content = clean_log_text(update_status.content)
        log_writer(
            room_id=room[1],
            room_alias=room[0],
            status="success",
            status_code=update_status.status_code,
            target=None,
            change_user=promote_user,
            old_pl=old_pl,
            new_pl=new_pl,
            content=content
        )

    # Log finished operation
    log_writer(
        room_id=None,
        room_alias=None,
        status="finished_operation",
        status_code=None,
        target=None,
        change_user=None,
        old_pl=None,
        new_pl=None,
        content="Operation finished"
    )
