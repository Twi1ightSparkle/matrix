# Import modules
import json
import logging
import os
import requests
import time
from tqdm import tqdm
from mass_upgrade_rooms_config import Config


if __name__ == "__main__":
    # Configure logging
    log_file_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "mass_upgrade_rooms.log")
    log_level = getattr(logging, Config.log_level.upper())
    logging.basicConfig(
        filename=log_file_path,
        format="%(asctime)s %(levelname)s %(message)s",
        level=log_level
    )

    # Headers to sent to the rest API
    headers = {
        "Authorization": "Bearer %s" % Config.admin_token,
        "Content-Type": "application/json"
    }

    # Loop over all rooms
    logging.debug("Config.rooms: %s" %Config.rooms)
    for room in tqdm(Config.rooms):
        room_alias, room_id = room

        # Clean Room ID
        room_id_safe = room_id.replace("!", "%21").replace(":", "%3A")
        logging.debug("room_id: %s" %room_id)

        # Check current room version
        state_url = "%s/_matrix/client/r0/rooms/%s/state/m.room.create" %(Config.homeserver_delegated_url, room_id_safe)
        logging.debug("state_url: %s" % state_url)
        try:
            m_room_create = requests.request(
                method="GET",
                url=state_url,
                headers=headers
            )
        except requests.exceptions.ConnectionError as err:
            logging.error("Unable to get current state for %s - %s" % (room_id, err))
            continue

        # If getting room state was successful
        if m_room_create.status_code == 200:
            m_room_create = m_room_create.json()
            logging.debug("m_room_create: %s" % m_room_create)
            # Skip to next room if no upgrade is needed
            if int(m_room_create["room_version"]) >= Config.new_room_version:
                logging.info("Skipping room with ID %s and alias %s. Already room version %s" % (room_id, room_alias, str(Config.new_room_version)))
                continue
        else:
            try: # Convert result to a dictionary
                m_room_create = m_room_create.json()
            except json.decoder.JSONDecodeError as err: # If not JSON
                logging.error("%s - %s - %s" % (room_id, room_alias, err))
            else: # If JSON
                m_room_create["room_id"] = room_id
                m_room_create["room_alias"] = room_alias
                logging.error(m_room_create)


        # Upgrade the room
        upgrade_url = "%s/_matrix/client/r0/rooms/%s/upgrade" %(Config.homeserver_delegated_url, room_id_safe)
        data = {"new_version": str(Config.new_room_version)}
        logging.debug("upgrade_url: %s - data: %s" % (upgrade_url, data))
        try:
            upgrade_result = requests.request(
                method="POST",
                url=upgrade_url,
                headers=headers,
                data=json.dumps(data)
            )
        except requests.exceptions.ConnectionError as err:
            logging.error("%s - %s" % (room_alias, err))
            exit()

        # If successful upgrade
        if upgrade_result.status_code == 200:
            upgrade_result = upgrade_result.json()
            logging.debug(upgrade_result)
            logging.info("Room %s successfully upgraded. Old Room ID: %s - New Room ID: %s" % (room_alias, room_id, upgrade_result["replacement_room"]))

            # Send a message to the old room
            message_url = "%s/_matrix/client/r0/rooms/%s/send/m.room.message" %(Config.homeserver_delegated_url, room_id_safe)
            data = {"msgtype": "m.text", "body": Config.message_template(upgrade_result["replacement_room"], room_alias)}
            logging.debug("message_url: %s - data: %s" %(message_url, data))
            try:
                message_result = requests.request(
                    method="POST",
                    url=message_url,
                    headers=headers,
                    data=json.dumps(data)
                )
            except requests.exceptions.ConnectionError as err:
                logging.error("%s - %s" % (room_alias, err))
                exit()

            # If sending message was successful
            if message_result.status_code == 200:
                logging.debug("message_result: %s" %message_result.json())
                logging.info("Successfully messaged room %s" %room_id)
            else:
                try: # Convert result to a dictionary
                    message_result = message_result.json()
                except json.decoder.JSONDecodeError as err: # If not JSON
                    logging.error("%s - %s - %s" % (room_id, room_alias, err))
                else: # If JSON
                    message_result["room_id"] = room_id
                    message_result["room_alias"] = room_alias
                    logging.error(message_result)

        # If error on upgrade
        else:
            try: # Convert result to a dictionary
                upgrade_result = upgrade_result.json()
            except json.decoder.JSONDecodeError as err: # If not JSON
                logging.error("%s - %s - %s" % (room_id, room_alias, err))
            else: # If JSON
                upgrade_result["room_id"] = room_id
                upgrade_result["room_alias"] = room_alias
                logging.error(upgrade_result)

        # Wait a minute to not get rate limited, and to not overwhelm the server
        time.sleep(60)
