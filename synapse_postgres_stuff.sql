-- Basic user info
SELECT
	name,
    creation_ts,
    admin,
    deactivated
FROM
	users
WHERE
	name = '@username:matrix.org';


-- Find uername from email
SELECT * FROM
	user_threepid_id_server
WHERE
	address = 'user@domain.tld';


-- Find email from username
SELECT * FROM
	user_threepid_id_server
WHERE
	user_id = '@username:matrix.org';


-- Find all rooms a user is member of
SELECT
    user_id, 
    room_id
FROM
    room_memberships
WHERE
    user_id = '@username:matrix.org' AND
    membership = 'join';


-- Find all rooms a user is member of v2
SELECT
	rm.room_id AS room_id,
	ra.room_alias AS room_alias
FROM
	room_memberships rm
FULL OUTER JOIN room_aliases ra ON rm.room_id = ra.room_id
WHERE
    rm.user_id = '@username:matrix.org' AND
    rm.membership = 'join';


-- uhhh something maybe?
SELECT
    rm.room_id     AS room_id,
    ra.room_alias  AS alias

FROM
    room_memberships                rm
FULL OUTER JOIN room_aliases        ra ON rm.room_id = ra.room_id
LEFT JOIN       room_stats_state    rs ON rm.room_id = rs.room_id
WHERE
    rm.user_id = '@username:matrix.org' AND
    ev.type = 'm.room.create';