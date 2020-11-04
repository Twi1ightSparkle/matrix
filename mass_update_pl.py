# Import modules
from datetime import datetime
import json
import os
import progressbar
import psycopg2
import requests


# Import config
from mass_update_pl_config import Config


# Log to this file. Default is result.csv in the same directory as this script file
log_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mass_update_pl.csv")


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
        log.write("Time Stamp;Room ID;Room Alias;Status;Status Code;Target URL;Promote User;Old PL;New PL;Content\n")
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
    connection = psycopg2.connect(
        user=Config.username,
        password=Config.password,
        host=Config.server,
        port=Config.port,
        database=Config.database,
        connect_timeout=3
    )
    cursor = connection.cursor()

    # Get list of rooms. Creates a list: [[room_alias, room_id], ...]
    rooms = []
    cursor.execute(Config.rooms_query)
    mobile_records = cursor.fetchall() 
    for row in mobile_records:
        rooms.append(row)


    # Log new operation
    if Config.dry_run:
        content_dry_run = " dry run"
    else:
        content_dry_run = ""
    log_writer(
        room_id="",
        room_alias="",
        status="new_operation",
        status_code="",
        target="",
        change_user="",
        old_pl="",
        new_pl="",
        content="New%s operation started. %s rooms to change" % (content_dry_run, len(rooms))
    )


    # Check if minus_pl or set_pl is set. This is done with try/except because
    # both can have value 0, which is False when doing "if minus_pl:"
    minus_pl_set = False
    set_pl_set = False
    try:
        Config.minus_pl
    except AttributeError: # minus_pl is not set
        try:
            Config.set_pl
        except AttributeError: # set_pl is not set
            print("One of minus_pl or new_pl must be uncommented in config. Exiting")
            log_writer(
                room_id="",
                room_alias="",
                status="pl_not_configured",
                status_code="",
                target="",
                change_user="",
                old_pl="",
                new_pl="",
                content="One of minus_pl or set_pl must be uncommented in config. Cancelled operation"
            )
            exit()
        else: # set_pl is set
            set_pl_set = True
    else: # minus_pl is set
            minus_pl_set = True

    # Loop over the rooms
    pbar = progressbar.ProgressBar(maxval=len(rooms)).start()
    for room in pbar(rooms):

        # Request URL and headers
        target = Config.homeserver_delegated_url + "/_matrix/client/r0/rooms/" + room[1] + "/state/m.room.power_levels"
        headers = {
            "Authorization": "Bearer %s" % Config.admin_token,
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
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                content=content
            )
            continue


        # Get the power_levels state event from requests data
        power_levels = power_levels.json()

        # Get current PL for promote_user or set room default if it does not have any in the room
        old_pl = power_levels.get("users", {}).get(Config.promote_user, power_levels.get("users_default"))

        # Get PL for admin_user and append promote_user to state event
        admin_current_pl = power_levels.get("users", {}).get(Config.admin_user, "not_found")


        # If admin_user is not found, log and move on to next room
        if admin_current_pl == "not_found":
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="admin_not_found",
                status_code="",
                target="",
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                content="Admin user (%s) not in room or m.room.power_levels missing 'users' object" % Config.admin_user
            )
            continue


        # Set new power level for promote_user
        if set_pl_set:
            new_pl = Config.set_pl
        elif minus_pl_set:
            new_pl = admin_current_pl - Config.minus_pl
        
        # Remove promote_user from state event if it will be changed to default PL
        if new_pl == power_levels.get("users_default") and power_levels["users"].get(Config.promote_user):
            del power_levels["users"][Config.promote_user]
        else:
            power_levels["users"][Config.promote_user] = new_pl


        # Log and move on to next room if no change will be made
        if old_pl == new_pl:
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="unchanged",
                status_code="",
                target="",
                change_user=Config.promote_user,
                old_pl=old_pl,
                new_pl="",
                content=""
            )
            continue


        # If trying to change to higher than or equal to admins PL, log and continue to next room
        if old_pl >= admin_current_pl:
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="pl_too_high",
                status_code="",
                target="",
                change_user=Config.promote_user,
                old_pl=old_pl,
                new_pl=new_pl,
                content="You cannot make changes to %s because it's current PL is equal to or higher than %s (PL %s)" %(Config.promote_user, Config.admin_user, admin_current_pl)
            )
            continue


        # Send new state event to the room
        if not Config.dry_run:
            update_status = requests.request(
                method="PUT",
                url=target,
                headers=headers,
                data=json.dumps(power_levels)
            )
        else:
            # Create dummy update_status object
            class update_status():
                status_code = 200
                content = "{'event_id':'$dry_run'}"


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
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                content=content
            )
            continue


        # Log success
        try:
            content = clean_log_text(update_status.json())
        except json.decoder.JSONDecodeError:
            content = clean_log_text(update_status.content)
        except AttributeError:
            # This will only occur on dry run, because the dummy update_status object does not have a .json() attribute
            content = clean_log_text(update_status.content)
        log_writer(
            room_id=room[1],
            room_alias=room[0],
            status="success",
            status_code=update_status.status_code,
            target="",
            change_user=Config.promote_user,
            old_pl=old_pl,
            new_pl=new_pl,
            content=content
        )


    # Log finished operation
    if Config.dry_run:
        content_dry_run = "Dry run "
    else:
        content_dry_run = ""
    log_writer(
        room_id="",
        room_alias="",
        status="finished_operation",
        status_code="",
        target="",
        change_user="",
        old_pl="",
        new_pl="",
        content="%sOperation finished" %content_dry_run
    )
