# Miscellaneous scripts for Matrix

Note: Developed on macOS Catalina using zsh shell. Compatibility with other shells/OS's is not guaranteed.

## continuously_reset_passwords.py
This has no real world uses. It is a CPU stress test for Synapse (it will likely crash your server). Password resets are very computationally expensive due to the several rounds of hashing. 

## create_matrix_users.py/txt
Quickly create a bunch of users on a matrix server using the Admin API. 1500 users takes about 5 minutes

## ems_check_dns_cors.sh
Check that DNS and CORS records are correct for a Modular Homeserver.  
Three arguments is required: hostname domain riotSubDomain  
Example: `./ems_check_dns_cors.sh twily01-staging twily.me element`

## mass_create_rooms.py
Create a bunch of rooms. They won't be sequentially numbered because of [this](https://github.com/matrix-org/synapse/issues/8309) Synapse bug. With default Synapse rate limiting, you will see speeds about one room per 10 seconds over a longer run.

## mass_update_pl.py
Based on rooms returned from a Postgres Query, change the power level for a user in the rooms. Also optionally invite the user to the rooms. Copy `mass_update_pl_config.example.py` to `mass_update_pl_config.py` and set your details before running. Testing this script in a development environment before running in production is strongly recommended.

## simulate_user_activity.py/txt
**Currently not finished and broken. I recommend you don't use it.**  
Quickly logs in with a bunch of users, joins a room and sends a message

## synapse_postgres_stuff.sql
Misc sql commands for looking up stuff in the Synapse postgres database
