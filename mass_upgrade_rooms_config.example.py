class Config():
    
    # Log level. INFO or DEBUG
    log_level = "INFO"

    # Homeserver URLs
    homeserver_delegated_url = "https://matrix.example.com"

    # User to make the room upgrade with, this user must have the correct permissions in the room. Usually 100 / Admin
    admin_token = "MDA..."

    # Upgrade to this room version
    new_room_version = 6

    # Template for message to send to old room. To cover for clients that does not support the tombstone event
    def message_template(new_room_id, room_alias):
        return "This room has been upgraded. The alias %s has been moved to the new room. The new room ID is %s" % (room_alias, new_room_id)

    # List of rooms to process. Format ["#primaryRoomAlias:localhost", "!roomID:localhost"],
    # Alias can be an empty string, only used for human readable log
    rooms = [
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
