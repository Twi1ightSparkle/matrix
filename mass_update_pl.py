# Import modules
from datetime import datetime
import json
import os
import psycopg2
import requests
import time
from tqdm import tqdm


# Import config
from mass_update_pl_config import Config


# Log to this file. Default is result.csv in the same directory as this script file
log_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mass_update_pl.csv")


def log_writer(room_id, room_alias, status, pl_status_code, in_status_code, target, change_user, old_pl, new_pl, pl_content, in_content):
    """Write timestamp and message to logfile"""
    time_stamp = datetime.utcnow()
    time_stamp_short = time_stamp.strftime("%Y.%m.%dT%H.%M.%S.%fZ")

    if os.path.isfile(log_file_path):
        csv_header = False
    else:
        csv_header = True

    log = open(log_file_path, "a+")

    if csv_header:
        log.write("Time Stamp;Room ID;Room Alias;Status;PL Status Code;Invite Status Code;Target URL;Promote User;Old PL;New PL;PL Content; Invite Content\n")
    log.write("%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s;%s\n" % (
        str(time_stamp_short),
        str(room_id),
        str(room_alias),
        str(status),
        str(pl_status_code),
        str(in_status_code),
        str(target),
        str(change_user),
        str(old_pl),
        str(new_pl),
        str(pl_content),
        str(in_content)
    ))
    log.close()


def clean_log_text(input_string):
    "Removes newlines, semi colons and double quotes to make line work with CSV log file"
    return str(input_string).replace("\n", "").replace(";", ":").replace("\"", "'")



if __name__ == "__main__":

    # Confirm write
    if not Config.dry_run:
        write_confirmation = input("Dry run disabled, proceed with write operation [y/N]: ")
        if not write_confirmation == "y":
            exit()

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
        pl_status_code="",
        in_status_code="",
        target="",
        change_user="",
        old_pl="",
        new_pl="",
        pl_content="New%s operation started. %s rooms to change" % (content_dry_run, len(rooms)),
        in_content=""
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
                pl_status_code="",
                in_status_code="",
                target="",
                change_user="",
                old_pl="",
                new_pl="",
                pl_content="One of minus_pl or set_pl must be uncommented in config. Cancelled operation",
                in_content=""
            )
            exit()
        else: # set_pl is set
            set_pl_set = True
    else: # minus_pl is set
            minus_pl_set = True

    # Rest headers
    headers = {
        "Authorization": "Bearer %s" % Config.admin_token,
        "Content-Type": "application/json"
    }

    # Get list of rooms admin_user is in
    admin_rooms = requests.request(
        method="GET",
        url=Config.homeserver_delegated_url + "/_matrix/client/r0/joined_rooms",
        headers=headers
    )

    # If error on GET rooms, log it and exit
    if not admin_rooms.status_code == 200:
        try:
            admin_rooms_content = clean_log_text(admin_rooms.json())
        except json.decoder.JSONDecodeError:
            admin_rooms_content = clean_log_text(admin_rooms.content)
        log_writer(
            room_id=room[1],
            room_alias=room[0],
            status="admin_rooms_get_error",
            pl_status_code=admin_rooms.status_code,
            in_status_code="",
            target=pl_target,
            change_user=Config.promote_user,
            old_pl="",
            new_pl="",
            pl_content=admin_rooms_content,
            in_content=""
        )
        exit()

    admin_rooms = admin_rooms.json()["joined_rooms"]


    if Config.invite and not Config.dry_run:
        print("Invite is enabled. To reduce server load, longer delay is set. Estimated runtime, up to %s minutes" %(len(rooms)))


    # Loop over the rooms
    for room in tqdm(rooms):

        # Check that admin_user is in room
        if not room[1] in admin_rooms:
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="admin_not_in_room",
                pl_status_code="",
                in_status_code="",
                target="",
                change_user="",
                old_pl="",
                new_pl="",
                pl_content="",
                in_content=""
            )
            continue


        # REST URLs and headers
        pl_target = Config.homeserver_delegated_url + "/_matrix/client/r0/rooms/" + room[1] + "/state/m.room.power_levels"
        members_target = Config.homeserver_delegated_url + "/_matrix/client/r0/rooms/" + room[1] + "/joined_members"
        invite_target = Config.homeserver_delegated_url + "/_matrix/client/r0/rooms/" + room[1] + "/invite"


        # Get current m.room.power_levels
        power_levels = requests.request(
            method="GET",
            url=pl_target,
            headers=headers
        )

        # If error on GET PL, log it and move on to next room
        if not power_levels.status_code == 200:
            try:
                pl_content = clean_log_text(power_levels.json())
            except json.decoder.JSONDecodeError:
                pl_content = clean_log_text(power_levels.content)
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="pl_get_error",
                pl_status_code=power_levels.status_code,
                in_status_code="",
                target=pl_target,
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                pl_content=pl_content,
                in_content=""
            )
            continue


        # Get current room members if enabled
        if Config.invite:
            members = requests.request(
                method="GET",
                url=members_target,
                headers=headers
            )

            # If error on GET members, log it and move on to next room
            if not members.status_code == 200:
                try:
                    member_content = clean_log_text(members.json())
                except json.decoder.JSONDecodeError:
                    member_content = clean_log_text(members.content)
                log_writer(
                    room_id=room[1],
                    room_alias=room[0],
                    status="members_get_error",
                    pl_status_code="",
                    in_status_code=members.status_code,
                    target=members_target,
                    change_user=Config.promote_user,
                    old_pl="",
                    new_pl="",
                    pl_content=member_content,
                    in_content=""
                )
                continue

            # Check if promote_user is in room already
            if Config.promote_user in members.json()["joined"]:
                invite_user = False
            else:
                invite_user = True


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
                pl_status_code="",
                in_status_code="",
                target="",
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                pl_content="Admin user (%s) not in room or m.room.power_levels missing 'users' object" % Config.admin_user,
                in_content=""
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
                status="pl_unchanged",
                pl_status_code="",
                in_status_code="",
                target="",
                change_user=Config.promote_user,
                old_pl=old_pl,
                new_pl="",
                pl_content="",
                in_content=""
            )
            continue


        # If trying to change to higher than or equal to admins PL, log and continue to next room
        if old_pl >= admin_current_pl:
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="pl_too_high",
                pl_status_code="",
                in_status_code="",
                target="",
                change_user=Config.promote_user,
                old_pl=old_pl,
                new_pl=new_pl,
                pl_content="You cannot make changes to %s because it's current PL is equal to or higher than %s (PL %s)" %(Config.promote_user, Config.admin_user, admin_current_pl),
                in_content=""
            )
            continue


        # Make live changes if not dry run
        if not Config.dry_run:
            # Invite user to room if needed
            if Config.invite and invite_user:
                invite_status = requests.request(
                    method='POST',
                    url=invite_target,
                    headers=headers,
                    data=json.dumps({"user_id": Config.promote_user})
                )

            # Send updated power_levels state event to the room
            update_status = requests.request(
                method="PUT",
                url=pl_target,
                headers=headers,
                data=json.dumps(power_levels)
            )
        else:
            # Create dummy status objects so logging works on dry run
            class invite_status():
                status_code = 200
                content = "{'event_id':'$dry_run'}"
            class update_status():
                status_code = 200
                content = "{'event_id':'$dry_run'}"

        # If error on invite, log it
        if invite_user and not invite_status.status_code == 200:
            try:
                in_content = clean_log_text(invite_status.json())
            except json.decoder.JSONDecodeError:
                in_content = clean_log_text(invite_status.content)
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="invite_error",
                pl_status_code="",
                in_status_code=invite_status.status_code,
                target=invite_target,
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                pl_content="",
                in_content=in_content
            )


        # If error on PL PUT, log it
        if not update_status.status_code == 200:
            try:
                pl_content = clean_log_text(update_status.json())
            except json.decoder.JSONDecodeError:
                pl_content = clean_log_text(update_status.content)
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="pl_put_error",
                pl_status_code=update_status.status_code,
                in_status_code="",
                target=pl_target,
                change_user=Config.promote_user,
                old_pl="",
                new_pl="",
                pl_content=pl_content,
                in_content=""
            )

        # Skip success logging of wither PUT failed
        if not update_status.status_code == 200 or (invite_user and not invite_status.status_code == 200):
            continue


        # Log success

        # Get PL write content
        try:
            pl_content = clean_log_text(update_status.json())
        except json.decoder.JSONDecodeError:
            pl_content = clean_log_text(update_status.content)
        except AttributeError:
            # This will only occur on dry run, because the dummy update_status object does not have a .json() attribute
            pl_content = clean_log_text(update_status.content)

        # If invite is enabled, get invite put content, then log both PL and invite success
        if Config.invite and invite_user:
            try:
                in_content = clean_log_text(invite_status.json())
            except json.decoder.JSONDecodeError:
                in_content = clean_log_text(invite_status.content)
            except AttributeError:
                # This will only occur on dry run, because the dummy invite_status object does not have a .json() attribute
                in_content = clean_log_text(invite_status.content)

            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="success",
                pl_status_code=update_status.status_code,
                in_status_code=invite_status.status_code,
                target="",
                change_user=Config.promote_user,
                old_pl=old_pl,
                new_pl=new_pl,
                pl_content=pl_content,
                in_content=in_content
            )

        # If invite is disabled, log only PL write content
        else:
            log_writer(
                room_id=room[1],
                room_alias=room[0],
                status="success",
                pl_status_code=update_status.status_code,
                in_status_code="-",
                target="",
                change_user=Config.promote_user,
                old_pl=old_pl,
                new_pl=new_pl,
                pl_content=pl_content,
                in_content="-"
            )


        # Add some delay to not get ratelimited when writing to the server
        if not Config.dry_run:
            if Config.invite and invite_user:
                time.sleep(60)
            else:
                time.sleep(1)


    # Log finished operation
    if Config.dry_run:
        content_dry_run = "Dry run "
    else:
        content_dry_run = ""
    log_writer(
        room_id="",
        room_alias="",
        status="finished_operation",
        pl_status_code="",
        in_status_code="",
        target="",
        change_user="",
        old_pl="",
        new_pl="",
        pl_content="%sOperation finished" %content_dry_run,
        in_content=""
    )
