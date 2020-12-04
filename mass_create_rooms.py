# Import modules
import json
import logging
import requests
import time


# Config
delegated_homeserver_url = "https://matrix.example.com"
homeserver_url = "example.com"
access_token = "secretKey"
room_prefix = "test_room_"
room_version = "6" # Must be in quotes
room_count = 25
log_level = "info" # DEBUG and INFO supported



def increment_list(a_list, index):
    """Increment the last integer in a list, then and appends it. Adds index+1 if list list is empty"""
    if len(a_list) == 0:
        a_list.append(index + 1)
    else:
        last_index = a_list[-1]
        a_list.append(last_index + 1)
    return a_list


if __name__ == "__main__":
    start = time.time()
    created_room_counter = 0
    log_level = getattr(logging, log_level.upper())
    logging.basicConfig(
        level=log_level,
        format="%(asctime)s %(levelname)s %(message)s",
        datefmt="%m/%d/%Y %I:%M:%S %p"
    )

    # Create a list with integers in range 1 to room_count + 1
    numbers = []
    for i in range(1, room_count + 1):
        numbers.append(i)

    # Headers to sent to the rest API
    url = "%s/_matrix/client/r0/createRoom" % delegated_homeserver_url
    headers = {
        "Authorization": "Bearer %s" % access_token,
        "Content-Type": "application/json"
    }
    logging.debug("numbers: %s\nurl: %s\nheaders: %s" %(numbers, url, headers))

    # Create rooms
    while True:
        # Remove first number from the list
        index = numbers.pop(0)

        # Set vars for ths room
        room_name = "%s%s" % (room_prefix, index)
        data = {
            "name": room_name,
            "room_alias_name": room_name,
            "visibility": "private",
            "room_version": room_version
        }
        logging.debug("index: %s\nroom_name: %s\ndata: %s" %(index, room_name, data))

        # Create room
        result = requests.request(
            method="POST",
            url=url,
            headers=headers,
            data=json.dumps(data)
        )
        logging.debug("result: %s" %result)

        # If room created successfully
        if result.status_code == 200:
            # Print some info
            created_room_counter += 1
            now = time.time()
            logging.info("Created %s out of %s rooms in %s seconds. Room name: %s" %(created_room_counter, room_count, int(now - start), room_name))

            # Exit program if the list is now empty
            if len(numbers) == 0:
                logging.debug("Breaking. numbers: %s" %numbers)
                break

        # If room not created successfully
        elif not result.status_code == 200:
            # Convert result to a dictionary
            try:
                result = result.json()
            
            # If not JSON, print an error for troubleshooting and continue
            except json.decoder.JSONDecodeError as err:
                logging.error(err)
                numbers = increment_list(numbers, index)
            
            # If JSON
            else:
                logging.debug("result: %s" %result)
                # If we got rate limited
                if result["errcode"] == "M_LIMIT_EXCEEDED":
                    numbers = increment_list(numbers, index)
                    logging.debug("nmbers: %s" %numbers)
                    # Wait the time we were requested to wait (+ half a second)
                    time.sleep((result["retry_after_ms"] + 500) / 1000)
                # If concent not accepted
                elif result["errcode"] == "M_CONSENT_NOT_GIVEN":
                    logging.error("Terms not accepted. Exiting")
                    exit(1)
        
        # Wait a bit because that is nice
        time.sleep(0.5)
