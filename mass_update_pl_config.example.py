class Config():
    
    # Homeserver URLs
    homeserver_delegated_url = "https://matrix.example.com"
    homeserver_url = "example.com"

    # Datbase config
    server = "127.0.0.1"
    port = 5432
    database = "synapse"
    username = "synapse"
    password = "V3ryS3cret"

    # User to make change with, this user should be admin in all rooms returned by rooms_query
    admin_user = "@alice:example.com"
    admin_token = "MDAxxxxxx"

    # User to promote in the rooms
    promote_user = "@bob:example.com"

    # Power level to set for promote_user. Uncomment one of minus_pl or set_pl
    #
    # Set PL relevant to the PL of admin_user. For example, minus_pl = 5 means promote_user will get the PL of admin_user - minus_pl
    # If you set it to 0, you will not be able to undo the change
    minus_pl = 5
    #
    # Promote promote_user to this specific power level.
    # Will not do anything if this is higher than what admin_user's PL is in the room
    # set_pl = 50

    # Also invite promote_user to the rooms? Runtime will be significantly longer.
    # A minute delay is added between each room where invited to avoid being joins rate limited or kneeling the server.
    # If you are inviting Mjolnir, make sure it will accept the invites from admin_user before running script.
    invite = True

    # Dry run, run through all rooms and log changes that would have been made, but don't actually change anything
    # The log will contain response code 200 and a dummy event ID
    dry_run = True

    # Format ["#primaryRoomAlias:localhost", "!roomID:localhost"],
    # Uncomment one of roomlist or rooms_query. If room_list is uncommented, rooms_query will be ignored
    room_list = [
        ["#room0:example.com", "!rCjhWzWtIAoAPmzKuQ:example.com"],
        ["#room1:example.com", "!BjjosTZswnbWcqaEJJ:example.com"],
        ["#room2:example.com", "!LQmdtmUtMLEBAGvMQW:example.com"],
        ["#room3:example.com", "!jJHFQJekwMQgZhMqKa:example.com"],
        ["#room4:example.com", "!DQzQAXbRYIwAMCtbCu:example.com"],
        ["#room5:example.com", "!xOuGeTUOHHITrvdcyD:example.com"],
        ["#room6:example.com", "!UANpAeMRFrwHNlqjxC:example.com"],
        ["#room7:example.com", "!XCLYvAajKdRukUsIph:example.com"],
        ["#room8:example.com", "!PTTqFpUfhkMpSYeLLQ:example.com"],
        ["#room9:example.com", "!YEOvNWPlmnvmvkFJVP:example.com"],
    ]


    # PostgreSQL query to get rooms to work with. Must return room_alias in column 0 and room_id in column 1
    rooms_query = """
        SELECT
            room_aliases.room_alias,
            rooms.room_id
        FROM
            rooms
            LEFT JOIN room_aliases ON rooms.room_id = room_aliases.room_id
        WHERE
            rooms.room_id IN(
                '!ivBXYrAnWXFuFTicZq:example.com',
                '!IQsmRFKOWWaGNVCmHU:example.com',
                '!impphkyzlXddOCpTvi:example.com'
            )
    """
