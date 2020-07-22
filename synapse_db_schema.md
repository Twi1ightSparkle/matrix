# Synapse Database Schema

Based on the live database of a large server running Synapse 1.17.0

## Table of Contents
<!-- TOC -->

- [Synapse Database Schema](#synapse-database-schema)
    - [Table of Contents](#table-of-contents)
    - [Table - access_tokens](#table---access_tokens)
    - [Table - account_data](#table---account_data)
    - [Table - account_data_max_stream_id](#table---account_data_max_stream_id)
    - [Table - account_validity](#table---account_validity)
    - [Table - application_services_state](#table---application_services_state)
    - [Table - application_services_txns](#table---application_services_txns)
    - [Table - applied_module_schemas](#table---applied_module_schemas)
    - [Table - applied_schema_deltas](#table---applied_schema_deltas)
    - [Table - appservice_room_list](#table---appservice_room_list)
    - [Table - appservice_stream_position](#table---appservice_stream_position)
    - [Table - background_updates](#table---background_updates)
    - [Table - blocked_rooms](#table---blocked_rooms)
    - [Table - cache_invalidation_stream](#table---cache_invalidation_stream)
    - [Table - cache_invalidation_stream_by_instance](#table---cache_invalidation_stream_by_instance)
    - [Table - current_state_delta_stream](#table---current_state_delta_stream)
    - [Table - current_state_events](#table---current_state_events)
    - [Table - deleted_pushers](#table---deleted_pushers)
    - [Table - destinations](#table---destinations)
    - [Table - device_federation_inbox](#table---device_federation_inbox)
    - [Table - device_federation_outbox](#table---device_federation_outbox)
    - [Table - device_inbox](#table---device_inbox)
    - [Table - device_lists_outbound_last_success](#table---device_lists_outbound_last_success)
    - [Table - device_lists_outbound_pokes](#table---device_lists_outbound_pokes)
    - [Table - device_lists_remote_cache](#table---device_lists_remote_cache)
    - [Table - device_lists_remote_extremeties](#table---device_lists_remote_extremeties)
    - [Table - device_lists_remote_resync](#table---device_lists_remote_resync)
    - [Table - device_lists_stream](#table---device_lists_stream)
    - [Table - device_max_stream_id](#table---device_max_stream_id)
    - [Table - devices](#table---devices)
    - [Table - e2e_cross_signing_keys](#table---e2e_cross_signing_keys)
    - [Table - e2e_cross_signing_signatures](#table---e2e_cross_signing_signatures)
    - [Table - e2e_device_keys_json](#table---e2e_device_keys_json)
    - [Table - e2e_one_time_keys_json](#table---e2e_one_time_keys_json)
    - [Table - e2e_room_keys](#table---e2e_room_keys)
    - [Table - e2e_room_keys_versions](#table---e2e_room_keys_versions)
    - [Table - erased_users](#table---erased_users)
    - [Table - event_auth](#table---event_auth)
    - [Table - event_backward_extremities](#table---event_backward_extremities)
    - [Table - event_edges](#table---event_edges)
    - [Table - event_expiry](#table---event_expiry)
    - [Table - event_forward_extremities](#table---event_forward_extremities)
    - [Table - event_json](#table---event_json)
    - [Table - event_labels](#table---event_labels)
    - [Table - event_push_actions](#table---event_push_actions)
    - [Table - event_push_actions_staging](#table---event_push_actions_staging)
    - [Table - event_push_summary](#table---event_push_summary)
    - [Table - event_push_summary_stream_ordering](#table---event_push_summary_stream_ordering)
    - [Table - event_reference_hashes](#table---event_reference_hashes)
    - [Table - event_relations](#table---event_relations)
    - [Table - event_reports](#table---event_reports)
    - [Table - event_search](#table---event_search)
    - [Table - event_to_state_groups](#table---event_to_state_groups)
    - [Table - events](#table---events)
    - [Table - ex_outlier_stream](#table---ex_outlier_stream)
    - [Table - federation_stream_position](#table---federation_stream_position)
    - [Table - group_attestations_remote](#table---group_attestations_remote)
    - [Table - group_attestations_renewals](#table---group_attestations_renewals)
    - [Table - group_invites](#table---group_invites)
    - [Table - group_roles](#table---group_roles)
    - [Table - group_room_categories](#table---group_room_categories)
    - [Table - group_rooms](#table---group_rooms)
    - [Table - group_summary_roles](#table---group_summary_roles)
    - [Table - group_summary_room_categories](#table---group_summary_room_categories)
    - [Table - group_summary_rooms](#table---group_summary_rooms)
    - [Table - group_summary_users](#table---group_summary_users)
    - [Table - group_users](#table---group_users)
    - [Table - groups](#table---groups)
    - [Table - local_current_membership](#table---local_current_membership)
    - [Table - local_group_membership](#table---local_group_membership)
    - [Table - local_group_updates](#table---local_group_updates)
    - [Table - local_invites](#table---local_invites)
    - [Table - local_media_repository](#table---local_media_repository)
    - [Table - local_media_repository_thumbnails](#table---local_media_repository_thumbnails)
    - [Table - local_media_repository_url_cache](#table---local_media_repository_url_cache)
    - [Table - monthly_active_users](#table---monthly_active_users)
    - [Table - open_id_tokens](#table---open_id_tokens)
    - [Table - presence](#table---presence)
    - [Table - presence_allow_inbound](#table---presence_allow_inbound)
    - [Table - presence_stream](#table---presence_stream)
    - [Table - profiles](#table---profiles)
    - [Table - public_room_list_stream](#table---public_room_list_stream)
    - [Table - push_rules](#table---push_rules)
    - [Table - push_rules_enable](#table---push_rules_enable)
    - [Table - push_rules_stream](#table---push_rules_stream)
    - [Table - pusher_throttle](#table---pusher_throttle)
    - [Table - pushers](#table---pushers)
    - [Table - ratelimit_override](#table---ratelimit_override)
    - [Table - receipts_graph](#table---receipts_graph)
    - [Table - receipts_linearized](#table---receipts_linearized)
    - [Table - received_transactions](#table---received_transactions)
    - [Table - redactions](#table---redactions)
    - [Table - rejections](#table---rejections)
    - [Table - remote_media_cache](#table---remote_media_cache)
    - [Table - remote_media_cache_thumbnails](#table---remote_media_cache_thumbnails)
    - [Table - remote_profile_cache](#table---remote_profile_cache)
    - [Table - room_account_data](#table---room_account_data)
    - [Table - room_alias_servers](#table---room_alias_servers)
    - [Table - room_aliases](#table---room_aliases)
    - [Table - room_depth](#table---room_depth)
    - [Table - room_memberships](#table---room_memberships)
    - [Table - room_retention](#table---room_retention)
    - [Table - room_stats_current](#table---room_stats_current)
    - [Table - room_stats_earliest_token](#table---room_stats_earliest_token)
    - [Table - room_stats_historical](#table---room_stats_historical)
    - [Table - room_stats_state](#table---room_stats_state)
    - [Table - room_tags](#table---room_tags)
    - [Table - room_tags_revisions](#table---room_tags_revisions)
    - [Table - rooms](#table---rooms)
    - [Table - schema_version](#table---schema_version)
    - [Table - server_keys_json](#table---server_keys_json)
    - [Table - server_signature_keys](#table---server_signature_keys)
    - [Table - state_events](#table---state_events)
    - [Table - state_group_edges](#table---state_group_edges)
    - [Table - state_groups](#table---state_groups)
    - [Table - state_groups_state](#table---state_groups_state)
    - [Table - stats_incremental_position](#table---stats_incremental_position)
    - [Table - stream_ordering_to_exterm](#table---stream_ordering_to_exterm)
    - [Table - threepid_guest_access_tokens](#table---threepid_guest_access_tokens)
    - [Table - threepid_validation_session](#table---threepid_validation_session)
    - [Table - threepid_validation_token](#table---threepid_validation_token)
    - [Table - ui_auth_sessions](#table---ui_auth_sessions)
    - [Table - ui_auth_sessions_credentials](#table---ui_auth_sessions_credentials)
    - [Table - user_daily_visits](#table---user_daily_visits)
    - [Table - user_directory](#table---user_directory)
    - [Table - user_directory_search](#table---user_directory_search)
    - [Table - user_directory_stream_pos](#table---user_directory_stream_pos)
    - [Table - user_external_ids](#table---user_external_ids)
    - [Table - user_filters](#table---user_filters)
    - [Table - user_ips](#table---user_ips)
    - [Table - user_signature_stream](#table---user_signature_stream)
    - [Table - user_stats_current](#table---user_stats_current)
    - [Table - user_stats_historical](#table---user_stats_historical)
    - [Table - user_threepid_id_server](#table---user_threepid_id_server)
    - [Table - user_threepids](#table---user_threepids)
    - [Table - users](#table---users)
    - [Table - users_in_public_rooms](#table---users_in_public_rooms)
    - [Table - users_pending_deactivation](#table---users_pending_deactivation)
    - [Table - users_who_share_private_rooms](#table---users_who_share_private_rooms)
    - [Sequence - cache_invalidation_stream_seq](#sequence---cache_invalidation_stream_seq)
    - [Sequence - state_group_id_seq](#sequence---state_group_id_seq)

<!-- /TOC -->

## Table - access_tokens
|     Column     |  Type  | Collation | Nullable | Default |
|----------------|--------|-----------|----------|---------|
| id             | bigint |           | not null | |
| user_id        | text   |           | not null | |
| device_id      | text   |           |          | |
| token          | text   |           | not null | |
| last_used      | bigint |           |          | |
| valid_until_ms | bigint |           |          | |

**Indexes**
* "access_tokens_pkey" PRIMARY KEY, btree (id)
* "access_tokens_token_key" UNIQUE CONSTRAINT, btree (token)
* "access_tokens_device_id" btree (user_id, device_id)


## Table - account_data
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| user_id           | text   |           | not null | |
| account_data_type | text   |           | not null | |
| stream_id         | bigint |           | not null | |
| content           | text   |           | not null | |

**Indexes**
* "account_data_uniqueness" UNIQUE CONSTRAINT, btree (user_id, account_data_type)
* "account_data_stream_id" btree (user_id, stream_id)


## Table - account_data_max_stream_id
|  Column   |     Type     | Collation | Nullable |   Default   |
|-----------|--------------|-----------|----------|-------------|
| lock      | character(1) |           | not null | 'X'::bpchar
| stream_id | bigint       |           | not null | |

**Indexes**
* "private_user_data_max_stream_id_lock_key" UNIQUE CONSTRAINT, btree (lock)

**Check constraints**
* "private_user_data_max_stream_id_lock_check" CHECK (lock = 'X'::bpchar)


## Table - account_validity
|      Column      |  Type   | Collation | Nullable | Default |
|------------------|---------|-----------|----------|---------|
| user_id          | text    |           | not null | |
| expiration_ts_ms | bigint  |           | not null | |
| email_sent       | boolean |           | not null | |
| renewal_token    | text    |           |          | |

**Indexes**
* "account_validity_pkey" PRIMARY KEY, btree (user_id)


## Table - application_services_state
|  Column  |         Type         | Collation | Nullable | Default |
|----------|----------------------|-----------|----------|---------|
| as_id    | text                 |           | not null | |
| state    | character varying(5) |           |          | |
| last_txn | integer              |           |          | |

**Indexes**
* "application_services_state_pkey" PRIMARY KEY, btree (as_id)


## Table - application_services_txns
|  Column   |  Type   | Collation | Nullable | Default |
|-----------|---------|-----------|----------|---------|
| as_id     | text    |           | not null | |
| txn_id    | integer |           | not null | |
| event_ids | text    |           | not null | |

**Indexes**
* "application_services_txns_as_id_txn_id_key" UNIQUE CONSTRAINT, btree (as_id, txn_id)
* "application_services_txns_id" btree (as_id)


## Table - applied_module_schemas
|   Column    | Type | Collation | Nullable | Default |
|-------------|------|-----------|----------|---------|
| module_name | text |           | not null | |
| file        | text |           | not null | |

**Indexes**
* "applied_module_schemas_module_name_file_key" UNIQUE CONSTRAINT, btree (module_name, file)


## Table - applied_schema_deltas
| Column  |  Type   | Collation | Nullable | Default |
|---------|---------|-----------|----------|---------|
| version | integer |           | not null | |
| file    | text    |           | not null | |

**Indexes**
* "applied_schema_deltas_version_file_key" UNIQUE CONSTRAINT, btree (version, file)


## Table - appservice_room_list
|    Column     | Type | Collation | Nullable | Default |
|---------------|------|-----------|----------|---------|
| appservice_id | text |           | not null | |
| network_id    | text |           | not null | |
| room_id       | text |           | not null | |

**Indexes**
* "appservice_room_list_idx" UNIQUE, btree (appservice_id, network_id, room_id)


## Table - appservice_stream_position
|     Column      |     Type     | Collation | Nullable |   Default   |
|-----------------|--------------|-----------|----------|-------------|
| lock            | character(1) |           | not null | 'X'::bpchar
| stream_ordering | bigint       |           |          | |

**Indexes**
* "appservice_stream_position_lock_key" UNIQUE CONSTRAINT, btree (lock)

**Check constraints**
* "appservice_stream_position_lock_check" CHECK (lock = 'X'::bpchar)


## Table - background_updates
|    Column     |  Type   | Collation | Nullable | Default |
|---------------|---------|-----------|----------|---------|
| update_name   | text    |           | not null | |
| progress_json | text    |           | not null | |
| depends_on    | text    |           |          | |
| ordering      | integer |           | not null | 0

**Indexes**
* "background_updates_uniqueness" UNIQUE CONSTRAINT, btree (update_name)


## Table - blocked_rooms
| Column  | Type | Collation | Nullable | Default |
|---------|------|-----------|----------|---------|
| room_id | text |           | not null | |
| user_id | text |           | not null | |

**Indexes**
* "blocked_rooms_idx" UNIQUE, btree (room_id)


## Table - cache_invalidation_stream
|     Column      |  Type  | Collation | Nullable | Default |
|-----------------|--------|-----------|----------|---------|
| stream_id       | bigint |           |          | |
| cache_func      | text   |           |          | |
| keys            | text[] |           |          | |
| invalidation_ts | bigint |           |          | |

**Indexes**
* "cache_invalidation_stream_id" btree (stream_id)


## Table - cache_invalidation_stream_by_instance
|     Column      |  Type  | Collation | Nullable | Default |
|-----------------|--------|-----------|----------|---------|
| stream_id       | bigint |           | not null | |
| instance_name   | text   |           | not null | |
| cache_func      | text   |           | not null | |
| keys            | text[] |           |          | |
| invalidation_ts | bigint |           |          | |

**Indexes**
* "cache_invalidation_stream_by_instance_id" UNIQUE, btree (stream_id)


## Table - current_state_delta_stream
|    Column     |  Type  | Collation | Nullable | Default |
|---------------|--------|-----------|----------|---------|
| stream_id     | bigint |           | not null | |
| room_id       | text   |           | not null | |
| type          | text   |           | not null | |
| state_key     | text   |           | not null | |
| event_id      | text   |           |          | |
| prev_event_id | text   |           |          | |

**Indexes**
* "current_state_delta_stream_idx" btree (stream_id)


## Table - current_state_events
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| event_id   | text |           | not null | |
| room_id    | text |           | not null | |
| type       | text |           | not null | |
| state_key  | text |           | not null | |
| membership | text |           |          | |

**Indexes**
* "current_state_events_event_id_key" UNIQUE CONSTRAINT, btree (event_id)
* "current_state_events_room_id_type_state_key_key" UNIQUE CONSTRAINT, btree (room_id, type, state_key)
* "current_state_events_member_index" btree (state_key) WHERE type = 'm.room.member'::text


## Table - deleted_pushers
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| stream_id | bigint |           | not null | |
| app_id    | text   |           | not null | |
| pushkey   | text   |           | not null | |
| user_id   | text   |           | not null | |

**Indexes**
* "deleted_pushers_stream_id" btree (stream_id)


## Table - destinations
|     Column     |  Type  | Collation | Nullable | Default |
|----------------|--------|-----------|----------|---------|
| destination    | text   |           | not null | |
| retry_last_ts  | bigint |           |          | |
| retry_interval | bigint |           |          | |
| failure_ts     | bigint |           |          | |

**Indexes**
* "destinations_pkey" PRIMARY KEY, btree (destination)


## Table - device_federation_inbox
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| origin      | text   |           | not null | |
| message_id  | text   |           | not null | |
| received_ts | bigint |           | not null | |

**Indexes**
* "device_federation_inbox_sender_id" btree (origin, message_id)


## Table - device_federation_outbox
|    Column     |  Type  | Collation | Nullable | Default |
|---------------|--------|-----------|----------|---------|
| destination   | text   |           | not null | |
| stream_id     | bigint |           | not null | |
| queued_ts     | bigint |           | not null | |
| messages_json | text   |           | not null | |

**Indexes**
* "device_federation_outbox_destination_id" btree (destination, stream_id)
* "device_federation_outbox_id" btree (stream_id)


## Table - device_inbox
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| user_id      | text   |           | not null | |
| device_id    | text   |           | not null | |
| stream_id    | bigint |           | not null | |
| message_json | text   |           | not null | |

**Indexes**
* "device_inbox_stream_id_user_id" btree (stream_id, user_id)
* "device_inbox_user_stream_id" btree (user_id, device_id, stream_id)


## Table - device_lists_outbound_last_success
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| destination | text   |           | not null | |
| user_id     | text   |           | not null | |
| stream_id   | bigint |           | not null | |

**Indexes**
* "device_lists_outbound_last_success_unique_idx" UNIQUE, btree (destination, user_id)


## Table - device_lists_outbound_pokes
|       Column        |  Type   | Collation | Nullable | Default |
|---------------------|---------|-----------|----------|---------|
| destination         | text    |           | not null | |
| stream_id           | bigint  |           | not null | |
| user_id             | text    |           | not null | |
| device_id           | text    |           | not null | |
| sent                | boolean |           | not null | |
| ts                  | bigint  |           | not null | |
| opentracing_context | text    |           |          | |

**Indexes**
* "device_lists_outbound_pokes_id" btree (destination, stream_id)
* "device_lists_outbound_pokes_stream" btree (stream_id)
* "device_lists_outbound_pokes_user" btree (destination, user_id)


## Table - device_lists_remote_cache
|  Column   | Type | Collation | Nullable | Default |
|-----------|------|-----------|----------|---------|
| user_id   | text |           | not null | |
| device_id | text |           | not null | |
| content   | text |           | not null | |

**Indexes**
* "device_lists_remote_cache_unique_id" UNIQUE, btree (user_id, device_id)


## Table - device_lists_remote_extremeties
|  Column   | Type | Collation | Nullable | Default |
|-----------|------|-----------|----------|---------|
| user_id   | text |           | not null | |
| stream_id | text |           | not null | |

**Indexes**
* "device_lists_remote_extremeties_unique_idx" UNIQUE, btree (user_id)


## Table - device_lists_remote_resync
|  Column  |  Type  | Collation | Nullable | Default |
|----------|--------|-----------|----------|---------|
| user_id  | text   |           | not null | |
| added_ts | bigint |           | not null | |

**Indexes**
* "device_lists_remote_resync_idx" UNIQUE, btree (user_id)
* "device_lists_remote_resync_ts_idx" btree (added_ts)


## Table - device_lists_stream
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| stream_id | bigint |           | not null | |
| user_id   | text   |           | not null | |
| device_id | text   |           | not null | |

**Indexes**
* "device_lists_stream_id" btree (stream_id, user_id)
* "device_lists_stream_user_id" btree (user_id, device_id)


## Table - device_max_stream_id
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| stream_id | bigint |           | not null | |


## Table - devices
|    Column    |  Type   | Collation | Nullable | Default |
|--------------|---------|-----------|----------|---------|
| user_id      | text    |           | not null | |
| device_id    | text    |           | not null | |
| display_name | text    |           |          | |
| last_seen    | bigint  |           |          | |
| ip           | text    |           |          | |
| user_agent   | text    |           |          | |
| hidden       | boolean |           |          | false

**Indexes**
* "device_uniqueness" UNIQUE CONSTRAINT, btree (user_id, device_id)


## Table - e2e_cross_signing_keys
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| user_id   | text   |           | not null | |
| keytype   | text   |           | not null | |
| keydata   | text   |           | not null | |
| stream_id | bigint |           | not null | |

**Indexes**
* "e2e_cross_signing_keys_idx" UNIQUE, btree (user_id, keytype, stream_id)


## Table - e2e_cross_signing_signatures
|      Column      | Type | Collation | Nullable | Default |
|------------------|------|-----------|----------|---------|
| user_id          | text |           | not null | |
| key_id           | text |           | not null | |
| target_user_id   | text |           | not null | |
| target_device_id | text |           | not null | |
| signature        | text |           | not null | |

**Indexes**
* "e2e_cross_signing_signatures2_idx" btree (user_id, target_user_id, target_device_id)


## Table - e2e_device_keys_json
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| user_id     | text   |           | not null | |
| device_id   | text   |           | not null | |
| ts_added_ms | bigint |           | not null | |
| key_json    | text   |           | not null | |

**Indexes**
* "e2e_device_keys_json_uniqueness" UNIQUE CONSTRAINT, btree (user_id, device_id)


## Table - e2e_one_time_keys_json
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| user_id     | text   |           | not null | |
| device_id   | text   |           | not null | |
| algorithm   | text   |           | not null | |
| key_id      | text   |           | not null | |
| ts_added_ms | bigint |           | not null | |
| key_json    | text   |           | not null | |

**Indexes**
* "e2e_one_time_keys_json_uniqueness" UNIQUE CONSTRAINT, btree (user_id, device_id, algorithm, key_id)


## Table - e2e_room_keys
|       Column        |  Type   | Collation | Nullable | Default |
|---------------------|---------|-----------|----------|---------|
| user_id             | text    |           | not null | |
| room_id             | text    |           | not null | |
| session_id          | text    |           | not null | |
| version             | bigint  |           | not null | |
| first_message_index | integer |           |          | |
| forwarded_count     | integer |           |          | |
| is_verified         | boolean |           |          | |
| session_data        | text    |           | not null | |

**Indexes**
* "e2e_room_keys_with_version_idx" UNIQUE, btree (user_id, version, room_id, session_id)


## Table - e2e_room_keys_versions
|  Column   |   Type   | Collation | Nullable | Default |
|-----------|----------|-----------|----------|---------|
| user_id   | text     |           | not null | |
| version   | bigint   |           | not null | |
| algorithm | text     |           | not null | |
| auth_data | text     |           | not null | |
| deleted   | smallint |           | not null | 0
| etag      | bigint   |           |          | |

**Indexes**
* "e2e_room_keys_versions_idx" UNIQUE, btree (user_id, version)


## Table - erased_users
| Column  | Type | Collation | Nullable | Default |
|---------|------|-----------|----------|---------|
| user_id | text |           | not null | |

**Indexes**
* "erased_users_user" UNIQUE, btree (user_id)


## Table - event_auth
|  Column  | Type | Collation | Nullable | Default |
|----------|------|-----------|----------|---------|
| event_id | text |           | not null | |
| auth_id  | text |           | not null | |
| room_id  | text |           | not null | |

**Indexes**
* "evauth_edges_id" btree (event_id)


## Table - event_backward_extremities
|  Column  | Type | Collation | Nullable | Default |
|----------|------|-----------|----------|---------|
| event_id | text |           | not null | |
| room_id  | text |           | not null | |

**Indexes**
* "event_backward_extremities_event_id_room_id_key" UNIQUE CONSTRAINT, btree (event_id, room_id)
* "ev_b_extrem_id" btree (event_id)
* "ev_b_extrem_room" btree (room_id)


## Table - event_edges
|    Column     |  Type   | Collation | Nullable | Default |
|---------------|---------|-----------|----------|---------|
| event_id      | text    |           | not null | |
| prev_event_id | text    |           | not null | |
| room_id       | text    |           | not null | |
| is_state      | boolean |           | not null | |

**Indexes**
* "event_edges_event_id_prev_event_id_room_id_is_state_key" UNIQUE CONSTRAINT, btree (event_id, prev_event_id, room_id, is_state)
* "ev_edges_id" btree (event_id)
* "ev_edges_prev_id" btree (prev_event_id)


## Table - event_expiry
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| event_id  | text   |           | not null | |
| expiry_ts | bigint |           | not null | |

**Indexes**
* "event_expiry_pkey" PRIMARY KEY, btree (event_id)
* "event_expiry_expiry_ts_idx" btree (expiry_ts)


## Table - event_forward_extremities
|  Column  | Type | Collation | Nullable | Default |
|----------|------|-----------|----------|---------|
| event_id | text |           | not null | |
| room_id  | text |           | not null | |

**Indexes**
* "event_forward_extremities_event_id_room_id_key" UNIQUE CONSTRAINT, btree (event_id, room_id)
* "ev_extrem_id" btree (event_id)
* "ev_extrem_room" btree (room_id)


## Table - event_json
|      Column       |  Type   | Collation | Nullable | Default |
|-------------------|---------|-----------|----------|---------|
| event_id          | text    |           | not null | |
| room_id           | text    |           | not null | |
| internal_metadata | text    |           | not null | |
| json              | text    |           | not null | |
| format_version    | integer |           |          | |

**Indexes**
* "event_json_event_id_key" UNIQUE CONSTRAINT, btree (event_id)
* "event_json_room_id" btree (room_id)


## Table - event_labels
|        Column        |  Type  | Collation | Nullable | Default |
|----------------------|--------|-----------|----------|---------|
| event_id             | text   |           | not null | |
| label                | text   |           | not null | |
| room_id              | text   |           | not null | |
| topological_ordering | bigint |           | not null | |

**Indexes**
* "event_labels_pkey" PRIMARY KEY, btree (event_id, label)
* "event_labels_room_id_label_idx" btree (room_id, label, topological_ordering)


## Table - event_push_actions
|        Column        |         Type          | Collation | Nullable | Default |
|----------------------|-----------------------|-----------|----------|---------|
| room_id              | text                  |           | not null | |
| event_id             | text                  |           | not null | |
| user_id              | text                  |           | not null | |
| profile_tag          | character varying(32) |           |          | |
| actions              | text                  |           | not null | |
| topological_ordering | bigint                |           |          | |
| stream_ordering      | bigint                |           |          | |
| notif                | smallint              |           |          | |
| highlight            | smallint              |           |          | |

**Indexes**
* "event_id_user_id_profile_tag_uniqueness" UNIQUE CONSTRAINT, btree (room_id, event_id, user_id, profile_tag)
* "event_push_actions_highlights_index" btree (user_id, room_id, topological_ordering, stream_ordering) WHERE highlight = 1
* "event_push_actions_rm_tokens" btree (user_id, room_id, topological_ordering, stream_ordering)
* "event_push_actions_room_id_user_id" btree (room_id, user_id)
* "event_push_actions_stream_ordering" btree (stream_ordering, user_id)
* "event_push_actions_u_highlight" btree (user_id, stream_ordering)


## Table - event_push_actions_staging
|  Column   |   Type   | Collation | Nullable | Default |
|-----------|----------|-----------|----------|---------|
| event_id  | text     |           | not null | |
| user_id   | text     |           | not null | |
| actions   | text     |           | not null | |
| notif     | smallint |           | not null | |
| highlight | smallint |           | not null | |

**Indexes**
* "event_push_actions_staging_id" btree (event_id)


## Table - event_push_summary
|     Column      |  Type  | Collation | Nullable | Default |
|-----------------|--------|-----------|----------|---------|
| user_id         | text   |           | not null | |
| room_id         | text   |           | not null | |
| notif_count     | bigint |           | not null | |
| stream_ordering | bigint |           | not null | |

**Indexes**
* "event_push_summary_user_rm" btree (user_id, room_id)


## Table - event_push_summary_stream_ordering
|     Column      |     Type     | Collation | Nullable |   Default   |
|-----------------|--------------|-----------|----------|-------------|
| lock            | character(1) |           | not null | 'X'::bpchar
| stream_ordering | bigint       |           | not null | |

**Indexes**
* "event_push_summary_stream_ordering_lock_key" UNIQUE CONSTRAINT, btree (lock)

**Check constraints**
* "event_push_summary_stream_ordering_lock_check" CHECK (lock = 'X'::bpchar)


## Table - event_reference_hashes
|  Column   | Type  | Collation | Nullable | Default |
|-----------|-------|-----------|----------|---------|
| event_id  | text  |           |          | |
| algorithm | text  |           |          | |
| hash      | bytea |           |          | |

**Indexes**
* "event_reference_hashes_event_id_algorithm_key" UNIQUE CONSTRAINT, btree (event_id, algorithm)
* "event_reference_hashes_id" btree (event_id)


## Table - event_relations
|     Column      | Type | Collation | Nullable | Default |
|-----------------|------|-----------|----------|---------|
| event_id        | text |           | not null | |
| relates_to_id   | text |           | not null | |
| relation_type   | text |           | not null | |
| aggregation_key | text |           |          | |

**Indexes**
* "event_relations_id" UNIQUE, btree (event_id)
* "event_relations_relates" btree (relates_to_id, relation_type, aggregation_key)


## Table - event_reports
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| id          | bigint |           | not null | |
| received_ts | bigint |           | not null | |
| room_id     | text   |           | not null | |
| event_id    | text   |           | not null | |
| user_id     | text   |           | not null | |
| reason      | text   |           |          | |
| content     | text   |           |          | |

**Indexes**
* "event_reports_pkey" PRIMARY KEY, btree (id)


## Table - event_search
|      Column      |   Type   | Collation | Nullable | Default |
|------------------|----------|-----------|----------|---------|
| event_id         | text     |           |          | |
| room_id          | text     |           |          | |
| sender           | text     |           |          | |
| key              | text     |           |          | |
| vector           | tsvector |           |          | |
| origin_server_ts | bigint   |           |          | |
| stream_ordering  | bigint   |           |          | |

**Indexes**
* "event_search_event_id_idx" UNIQUE, btree (event_id)
* "event_search_ev_ridx" btree (room_id)
* "event_search_fts_idx" gin (vector)


## Table - event_to_state_groups
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| event_id    | text   |           | not null | |
| state_group | bigint |           | not null | |

**Indexes**
* "event_to_state_groups_event_id_key" UNIQUE CONSTRAINT, btree (event_id)
* "event_to_state_groups_sg_index" btree (state_group)


## Table - events
|        Column        |  Type   | Collation | Nullable | Default |
|----------------------|---------|-----------|----------|---------|
| stream_ordering      | integer |           | not null | |
| topological_ordering | bigint  |           | not null | |
| event_id             | text    |           | not null | |
| type                 | text    |           | not null | |
| room_id              | text    |           | not null | |
| content              | text    |           |          | |
| unrecognized_keys    | text    |           |          | |
| processed            | boolean |           | not null | |
| outlier              | boolean |           | not null | |
| depth                | bigint  |           | not null | 0
| origin_server_ts     | bigint  |           |          | |
| received_ts          | bigint  |           |          | |
| sender               | text    |           |          | |
| contains_url         | boolean |           |          | |

**Indexes**
* "events_pkey" PRIMARY KEY, btree (stream_ordering)
* "events_event_id_key" UNIQUE CONSTRAINT, btree (event_id)
* "event_contains_url_index" btree (room_id, topological_ordering, stream_ordering) WHERE contains_url = true AND outlier = false
* "events_order_room" btree (room_id, topological_ordering, stream_ordering)
* "events_room_stream" btree (room_id, stream_ordering)
* "events_ts" btree (origin_server_ts, stream_ordering)


## Table - ex_outlier_stream
|        Column         |  Type  | Collation | Nullable | Default |
|-----------------------|--------|-----------|----------|---------|
| event_stream_ordering | bigint |           | not null | |
| event_id              | text   |           | not null | |
| state_group           | bigint |           | not null | |

**Indexes**
* "ex_outlier_stream_pkey" PRIMARY KEY, btree (event_stream_ordering)


## Table - federation_stream_position
|  Column   |  Type   | Collation | Nullable | Default |
|-----------|---------|-----------|----------|---------|
| type      | text    |           | not null | |
| stream_id | integer |           | not null | |


## Table - group_attestations_remote
|      Column      |  Type  | Collation | Nullable | Default |
|------------------|--------|-----------|----------|---------|
| group_id         | text   |           | not null | |
| user_id          | text   |           | not null | |
| valid_until_ms   | bigint |           | not null | |
| attestation_json | text   |           | not null | |

**Indexes**
* "group_attestations_remote_g_idx" btree (group_id, user_id)
* "group_attestations_remote_u_idx" btree (user_id)
* "group_attestations_remote_v_idx" btree (valid_until_ms)


## Table - group_attestations_renewals
|     Column     |  Type  | Collation | Nullable | Default |
|----------------|--------|-----------|----------|---------|
| group_id       | text   |           | not null | |
| user_id        | text   |           | not null | |
| valid_until_ms | bigint |           | not null | |

**Indexes**
* "group_attestations_renewals_g_idx" btree (group_id, user_id)
* "group_attestations_renewals_u_idx" btree (user_id)
* "group_attestations_renewals_v_idx" btree (valid_until_ms)


## Table - group_invites
|  Column  | Type | Collation | Nullable | Default |
|----------|------|-----------|----------|---------|
| group_id | text |           | not null | |
| user_id  | text |           | not null | |

**Indexes**
* "group_invites_g_idx" UNIQUE, btree (group_id, user_id)
* "group_invites_u_idx" btree (user_id)


## Table - group_roles
|  Column   |  Type   | Collation | Nullable | Default |
|-----------|---------|-----------|----------|---------|
| group_id  | text    |           | not null | |
| role_id   | text    |           | not null | |
| profile   | text    |           | not null | |
| is_public | boolean |           | not null | |

**Indexes**
* "group_roles_group_id_role_id_key" UNIQUE CONSTRAINT, btree (group_id, role_id)


## Table - group_room_categories
|   Column    |  Type   | Collation | Nullable | Default |
|-------------|---------|-----------|----------|---------|
| group_id    | text    |           | not null | |
| category_id | text    |           | not null | |
| profile     | text    |           | not null | |
| is_public   | boolean |           | not null | |

**Indexes**
* "group_room_categories_group_id_category_id_key" UNIQUE CONSTRAINT, btree (group_id, category_id)


## Table - group_rooms
|  Column   |  Type   | Collation | Nullable | Default |
|-----------|---------|-----------|----------|---------|
| group_id  | text    |           | not null | |
| room_id   | text    |           | not null | |
| is_public | boolean |           | not null | |

**Indexes**
* "group_rooms_g_idx" UNIQUE, btree (group_id, room_id)
* "group_rooms_r_idx" btree (room_id)


## Table - group_summary_roles
|   Column   |  Type  | Collation | Nullable | Default |
|------------|--------|-----------|----------|---------|
| group_id   | text   |           | not null | |
| role_id    | text   |           | not null | |
| role_order | bigint |           | not null | |

**Indexes**
* "group_summary_roles_group_id_role_id_role_order_key" UNIQUE CONSTRAINT, btree (group_id, role_id, role_order)

**Check constraints**
* "group_summary_roles_role_order_check" CHECK (role_order > 0)


## Table - group_summary_room_categories
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| group_id    | text   |           | not null | |
| category_id | text   |           | not null | |
| cat_order   | bigint |           | not null | |

**Indexes**
* "group_summary_room_categories_group_id_category_id_cat_orde_key" UNIQUE CONSTRAINT, btree (group_id, category_id, cat_order)

**Check constraints**
* "group_summary_room_categories_cat_order_check" CHECK (cat_order > 0)


## Table - group_summary_rooms
|   Column    |  Type   | Collation | Nullable | Default |
|-------------|---------|-----------|----------|---------|
| group_id    | text    |           | not null | |
| room_id     | text    |           | not null | |
| category_id | text    |           | not null | |
| room_order  | bigint  |           | not null | |
| is_public   | boolean |           | not null | |

**Indexes**
* "group_summary_rooms_g_idx" UNIQUE, btree (group_id, room_id, category_id)
* "group_summary_rooms_group_id_category_id_room_id_room_order_key" UNIQUE CONSTRAINT, btree (group_id, category_id, room_id, room_order)

**Check constraints**
* "group_summary_rooms_room_order_check" CHECK (room_order > 0)


## Table - group_summary_users
|   Column   |  Type   | Collation | Nullable | Default |
|------------|---------|-----------|----------|---------|
| group_id   | text    |           | not null | |
| user_id    | text    |           | not null | |
| role_id    | text    |           | not null | |
| user_order | bigint  |           | not null | |
| is_public  | boolean |           | not null | |

**Indexes**
* "group_summary_users_g_idx" btree (group_id)


## Table - group_users
|  Column   |  Type   | Collation | Nullable | Default |
|-----------|---------|-----------|----------|---------|
| group_id  | text    |           | not null | |
| user_id   | text    |           | not null | |
| is_admin  | boolean |           | not null | |
| is_public | boolean |           | not null | |

**Indexes**
* "group_users_g_idx" UNIQUE, btree (group_id, user_id)
* "group_users_u_idx" btree (user_id)


## Table - groups
|      Column       |  Type   | Collation | Nullable |    Default     |
|-------------------|---------|-----------|----------|----------------|
| group_id          | text    |           | not null | |
| name              | text    |           |          | |
| avatar_url        | text    |           |          | |
| short_description | text    |           |          | |
| long_description  | text    |           |          | |
| is_public         | boolean |           | not null | |
| join_policy       | text    |           | not null | 'invite'::text

**Indexes**
* "groups_idx" UNIQUE, btree (group_id)


## Table - local_current_membership
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| room_id    | text |           | not null | |
| user_id    | text |           | not null | |
| event_id   | text |           | not null | |
| membership | text |           | not null | |

**Indexes**
* "local_current_membership_idx" UNIQUE, btree (user_id, room_id)
* "local_current_membership_room_idx" btree (room_id)


## Table - local_group_membership
|    Column     |  Type   | Collation | Nullable | Default |
|---------------|---------|-----------|----------|---------|
| group_id      | text    |           | not null | |
| user_id       | text    |           | not null | |
| is_admin      | boolean |           | not null | |
| membership    | text    |           | not null | |
| is_publicised | boolean |           | not null | |
| content       | text    |           | not null | |

**Indexes**
* "local_group_membership_g_idx" btree (group_id)
* "local_group_membership_u_idx" btree (user_id, group_id)


## Table - local_group_updates
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| stream_id | bigint |           | not null | |
| group_id  | text   |           | not null | |
| user_id   | text   |           | not null | |
| type      | text   |           | not null | |
| content   | text   |           | not null | |


## Table - local_invites
|      Column      |  Type  | Collation | Nullable | Default |
|------------------|--------|-----------|----------|---------|
| stream_id        | bigint |           | not null | |
| inviter          | text   |           | not null | |
| invitee          | text   |           | not null | |
| event_id         | text   |           | not null | |
| room_id          | text   |           | not null | |
| locally_rejected | text   |           |          | |
| replaced_by      | text   |           |          | |

**Indexes**
* "local_invites_for_user_idx" btree (invitee, locally_rejected, replaced_by, room_id)
* "local_invites_id" btree (stream_id)


## Table - local_media_repository
|        Column        |  Type   | Collation | Nullable | Default |
|----------------------|---------|-----------|----------|---------|
| media_id             | text    |           |          | |
| media_type           | text    |           |          | |
| media_length         | integer |           |          | |
| created_ts           | bigint  |           |          | |
| upload_name          | text    |           |          | |
| user_id              | text    |           |          | |
| quarantined_by       | text    |           |          | |
| url_cache            | text    |           |          | |
| last_access_ts       | bigint  |           |          | |
| safe_from_quarantine | boolean |           | not null | false

**Indexes**
* "local_media_repository_media_id_key" UNIQUE CONSTRAINT, btree (media_id)
* "local_media_repository_url_idx" btree (created_ts) WHERE url_cache IS NOT NULL


## Table - local_media_repository_thumbnails
|      Column      |  Type   | Collation | Nullable | Default |
|------------------|---------|-----------|----------|---------|
| media_id         | text    |           |          | |
| thumbnail_width  | integer |           |          | |
| thumbnail_height | integer |           |          | |
| thumbnail_type   | text    |           |          | |
| thumbnail_method | text    |           |          | |
| thumbnail_length | integer |           |          | |

**Indexes**
* "local_media_repository_thumbn_media_id_thumbnail_width_thum_key" UNIQUE CONSTRAINT, btree (media_id, thumbnail_width, thumbnail_height, thumbnail_type)
* "local_media_repository_thumbnails_media_id" btree (media_id)


## Table - local_media_repository_url_cache
|    Column     |  Type   | Collation | Nullable | Default |
|---------------|---------|-----------|----------|---------|
| url           | text    |           |          | |
| response_code | integer |           |          | |
| etag          | text    |           |          | |
| expires_ts    | bigint  |           |          | |
| og            | text    |           |          | |
| media_id      | text    |           |          | |
| download_ts   | bigint  |           |          | |

**Indexes**
* "local_media_repository_url_cache_by_url_download_ts" btree (url, download_ts)
* "local_media_repository_url_cache_expires_idx" btree (expires_ts)
* "local_media_repository_url_cache_media_idx" btree (media_id)


## Table - monthly_active_users
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| user_id   | text   |           | not null | |
| timestamp | bigint |           | not null | |

**Indexes**
* "monthly_active_users_users" UNIQUE, btree (user_id)
* "monthly_active_users_time_stamp" btree ("timestamp")


## Table - open_id_tokens
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| token             | text   |           | not null | |
| ts_valid_until_ms | bigint |           | not null | |
| user_id           | text   |           | not null | |

**Indexes**
* "open_id_tokens_pkey" PRIMARY KEY, btree (token)
* "open_id_tokens_ts_valid_until_ms" btree (ts_valid_until_ms)


## Table - presence
|   Column   |         Type          | Collation | Nullable | Default |
|------------|-----------------------|-----------|----------|---------|
| user_id    | text                  |           | not null | |
| state      | character varying(20) |           |          | |
| status_msg | text                  |           |          | |
| mtime      | bigint                |           |          | |

**Indexes**
* "presence_user_id_key" UNIQUE CONSTRAINT, btree (user_id)


## Table - presence_allow_inbound
|      Column      | Type | Collation | Nullable | Default |
|------------------|------|-----------|----------|---------|
| observed_user_id | text |           | not null | |
| observer_user_id | text |           | not null | |

**Indexes**
* "presence_allow_inbound_observed_user_id_observer_user_id_key" UNIQUE CONSTRAINT, btree (observed_user_id, observer_user_id)


## Table - presence_stream
|          Column           |  Type   | Collation | Nullable | Default |
|---------------------------|---------|-----------|----------|---------|
| stream_id                 | bigint  |           |          | |
| user_id                   | text    |           |          | |
| state                     | text    |           |          | |
| last_active_ts            | bigint  |           |          | |
| last_federation_update_ts | bigint  |           |          | |
| last_user_sync_ts         | bigint  |           |          | |
| status_msg                | text    |           |          | |
| currently_active          | boolean |           |          | |

**Indexes**
* "presence_stream_id" btree (stream_id, user_id)
* "presence_stream_user_id" btree (user_id)


## Table - profiles
|   Column    | Type | Collation | Nullable | Default |
|-------------|------|-----------|----------|---------|
| user_id     | text |           | not null | |
| displayname | text |           |          | |
| avatar_url  | text |           |          | |

**Indexes**
* "profiles_user_id_key" UNIQUE CONSTRAINT, btree (user_id)


## Table - public_room_list_stream
|    Column     |  Type   | Collation | Nullable | Default |
|---------------|---------|-----------|----------|---------|
| stream_id     | bigint  |           | not null | |
| room_id       | text    |           | not null | |
| visibility    | boolean |           | not null | |
| appservice_id | text    |           |          | |
| network_id    | text    |           |          | |

**Indexes**
* "public_room_list_stream_idx" btree (stream_id)
* "public_room_list_stream_network" btree (appservice_id, network_id, room_id)
* "public_room_list_stream_rm_idx" btree (room_id, stream_id)


## Table - push_rules
|     Column     |   Type   | Collation | Nullable | Default |
|----------------|----------|-----------|----------|---------|
| id             | bigint   |           | not null | |
| user_name      | text     |           | not null | |
| rule_id        | text     |           | not null | |
| priority_class | smallint |           | not null | |
| priority       | integer  |           | not null | 0
| conditions     | text     |           | not null | |
| actions        | text     |           | not null | |

**Indexes**
* "push_rules_pkey" PRIMARY KEY, btree (id)
* "push_rules_user_name_rule_id_key" UNIQUE CONSTRAINT, btree (user_name, rule_id)
* "push_rules_user_name" btree (user_name)


## Table - push_rules_enable
|  Column   |   Type   | Collation | Nullable | Default |
|-----------|----------|-----------|----------|---------|
| id        | bigint   |           | not null | |
| user_name | text     |           | not null | |
| rule_id   | text     |           | not null | |
| enabled   | smallint |           |          | |

**Indexes**
* "push_rules_enable_pkey" PRIMARY KEY, btree (id)
* "push_rules_enable_user_name_rule_id_key" UNIQUE CONSTRAINT, btree (user_name, rule_id)
* "push_rules_enable_user_name" btree (user_name)


## Table - push_rules_stream
|        Column         |   Type   | Collation | Nullable | Default |
|-----------------------|----------|-----------|----------|---------|
| stream_id             | bigint   |           | not null | |
| event_stream_ordering | bigint   |           | not null | |
| user_id               | text     |           | not null | |
| rule_id               | text     |           | not null | |
| op                    | text     |           | not null | |
| priority_class        | smallint |           |          | |
| priority              | integer  |           |          | |
| conditions            | text     |           |          | |
| actions               | text     |           |          | |

**Indexes**
* "push_rules_stream_id" btree (stream_id)
* "push_rules_stream_user_stream_id" btree (user_id, stream_id)


## Table - pusher_throttle
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| pusher       | bigint |           | not null | |
| room_id      | text   |           | not null | |
| last_sent_ts | bigint |           |          | |
| throttle_ms  | bigint |           |          | |

**Indexes**
* "pusher_throttle_pkey" PRIMARY KEY, btree (pusher, room_id)


## Table - pushers
|        Column        |  Type   | Collation | Nullable | Default |
|----------------------|---------|-----------|----------|---------|
| id                   | bigint  |           | not null | |
| user_name            | text    |           | not null | |
| access_token         | bigint  |           |          | |
| profile_tag          | text    |           | not null | |
| kind                 | text    |           | not null | |
| app_id               | text    |           | not null | |
| app_display_name     | text    |           | not null | |
| device_display_name  | text    |           | not null | |
| pushkey              | text    |           | not null | |
| ts                   | bigint  |           | not null | |
| lang                 | text    |           |          | |
| data                 | text    |           |          | |
| last_stream_ordering | integer |           |          | |
| last_success         | bigint  |           |          | |
| failing_since        | bigint  |           |          | |

**Indexes**
* "pushers2_pkey" PRIMARY KEY, btree (id)
* "pushers2_app_id_pushkey_user_name_key" UNIQUE CONSTRAINT, btree (app_id, pushkey, user_name)


## Table - ratelimit_override
|       Column        |  Type  | Collation | Nullable | Default |
|---------------------|--------|-----------|----------|---------|
| user_id             | text   |           | not null | |
| messages_per_second | bigint |           |          | |
| burst_count         | bigint |           |          | |

**Indexes**
* "ratelimit_override_idx" UNIQUE, btree (user_id)


## Table - receipts_graph
|    Column    | Type | Collation | Nullable | Default |
|--------------|------|-----------|----------|---------|
| room_id      | text |           | not null | |
| receipt_type | text |           | not null | |
| user_id      | text |           | not null | |
| event_ids    | text |           | not null | |
| data         | text |           | not null | |

**Indexes**
* "receipts_graph_uniqueness" UNIQUE CONSTRAINT, btree (room_id, receipt_type, user_id)


## Table - receipts_linearized
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| stream_id    | bigint |           | not null | |
| room_id      | text   |           | not null | |
| receipt_type | text   |           | not null | |
| user_id      | text   |           | not null | |
| event_id     | text   |           | not null | |
| data         | text   |           | not null | |

**Indexes**
* "receipts_linearized_uniqueness" UNIQUE CONSTRAINT, btree (room_id, receipt_type, user_id)
* "receipts_linearized_id" btree (stream_id)
* "receipts_linearized_room_stream" btree (room_id, stream_id)
* "receipts_linearized_user" btree (user_id)


## Table - received_transactions
|       Column        |   Type   | Collation | Nullable | Default |
|---------------------|----------|-----------|----------|---------|
| transaction_id      | text     |           |          | |
| origin              | text     |           |          | |
| ts                  | bigint   |           |          | |
| response_code       | integer  |           |          | |
| response_json       | bytea    |           |          | |
| has_been_referenced | smallint |           |          | 0

**Indexes**
* "received_transactions_transaction_id_origin_key" UNIQUE CONSTRAINT, btree (transaction_id, origin)
* "received_transactions_ts" btree (ts)


## Table - redactions
|    Column     |  Type   | Collation | Nullable | Default |
|---------------|---------|-----------|----------|---------|
| event_id      | text    |           | not null | |
| redacts       | text    |           | not null | |
| have_censored | boolean |           | not null | false
| received_ts   | bigint  |           |          | |

**Indexes**
* "redactions_event_id_key" UNIQUE CONSTRAINT, btree (event_id)
* "redactions_have_censored_ts" btree (received_ts) WHERE NOT have_censored
* "redactions_redacts" btree (redacts)


## Table - rejections
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| event_id   | text |           | not null | |
| reason     | text |           | not null | |
| last_check | text |           | not null | |

**Indexes**
* "rejections_event_id_key" UNIQUE CONSTRAINT, btree (event_id)


## Table - remote_media_cache
|     Column     |  Type   | Collation | Nullable | Default |
|----------------|---------|-----------|----------|---------|
| media_origin   | text    |           |          | |
| media_id       | text    |           |          | |
| media_type     | text    |           |          | |
| created_ts     | bigint  |           |          | |
| upload_name    | text    |           |          | |
| media_length   | integer |           |          | |
| filesystem_id  | text    |           |          | |
| last_access_ts | bigint  |           |          | |
| quarantined_by | text    |           |          | |

**Indexes**
* "remote_media_cache_media_origin_media_id_key" UNIQUE CONSTRAINT, btree (media_origin, media_id)


## Table - remote_media_cache_thumbnails
|      Column      |  Type   | Collation | Nullable | Default |
|------------------|---------|-----------|----------|---------|
| media_origin     | text    |           |          | |
| media_id         | text    |           |          | |
| thumbnail_width  | integer |           |          | |
| thumbnail_height | integer |           |          | |
| thumbnail_method | text    |           |          | |
| thumbnail_type   | text    |           |          | |
| thumbnail_length | integer |           |          | |
| filesystem_id    | text    |           |          | |

**Indexes**
* "remote_media_cache_thumbnails_media_origin_media_id_thumbna_key" UNIQUE CONSTRAINT, btree (media_origin, media_id, thumbnail_width, thumbnail_height, thumbnail_type)


## Table - remote_profile_cache
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| user_id     | text   |           | not null | |
| displayname | text   |           |          | |
| avatar_url  | text   |           |          | |
| last_check  | bigint |           | not null | |

**Indexes**
* "remote_profile_cache_user_id" UNIQUE, btree (user_id)
* "remote_profile_cache_time" btree (last_check)


## Table - room_account_data
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| user_id           | text   |           | not null | |
| room_id           | text   |           | not null | |
| account_data_type | text   |           | not null | |
| stream_id         | bigint |           | not null | |
| content           | text   |           | not null | |

**Indexes**
* "room_account_data_uniqueness" UNIQUE CONSTRAINT, btree (user_id, room_id, account_data_type)
* "room_account_data_stream_id" btree (user_id, stream_id)


## Table - room_alias_servers
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| room_alias | text |           | not null | |
| server     | text |           | not null | |

**Indexes**
* "room_alias_servers_alias" btree (room_alias)


## Table - room_aliases
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| room_alias | text |           | not null | |
| room_id    | text |           | not null | |
| creator    | text |           |          | |

**Indexes**
* "room_aliases_room_alias_key" UNIQUE CONSTRAINT, btree (room_alias)
* "room_aliases_id" btree (room_id)


## Table - room_depth
|  Column   |  Type   | Collation | Nullable | Default |
|-----------|---------|-----------|----------|---------|
| room_id   | text    |           | not null | |
| min_depth | integer |           | not null | |

**Indexes**
* "room_depth_room_id_key" UNIQUE CONSTRAINT, btree (room_id)
* "room_depth_room" btree (room_id)


## Table - room_memberships
|    Column    |  Type   | Collation | Nullable | Default |
|--------------|---------|-----------|----------|---------|
| event_id     | text    |           | not null | |
| user_id      | text    |           | not null | |
| sender       | text    |           | not null | |
| room_id      | text    |           | not null | |
| membership   | text    |           | not null | |
| forgotten    | integer |           |          | 0
| display_name | text    |           |          | |
| avatar_url   | text    |           |          | |

**Indexes**
* "room_memberships_event_id_key" UNIQUE CONSTRAINT, btree (event_id)
* "room_memberships_room_id" btree (room_id)
* "room_memberships_user_id" btree (user_id)
* "room_memberships_user_room_forgotten" btree (user_id, room_id) WHERE forgotten = 1


## Table - room_retention
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| room_id      | text   |           | not null | |
| event_id     | text   |           | not null | |
| min_lifetime | bigint |           |          | |
| max_lifetime | bigint |           |          | |

**Indexes**
* "room_retention_pkey" PRIMARY KEY, btree (room_id, event_id)
* "room_retention_max_lifetime_idx" btree (max_lifetime)


## Table - room_stats_current
|          Column           |  Type   | Collation | Nullable | Default |
|---------------------------|---------|-----------|----------|---------|
| room_id                   | text    |           | not null | |
| current_state_events      | integer |           | not null | |
| joined_members            | integer |           | not null | |
| invited_members           | integer |           | not null | |
| left_members              | integer |           | not null | |
| banned_members            | integer |           | not null | |
| local_users_in_room       | integer |           | not null | |
| completed_delta_stream_id | bigint  |           | not null | |

**Indexes**
* "room_stats_current_pkey" PRIMARY KEY, btree (room_id)


## Table - room_stats_earliest_token
| Column  |  Type  | Collation | Nullable | Default |
|---------|--------|-----------|----------|---------|
| room_id | text   |           | not null | |
| token   | bigint |           | not null | |

**Indexes**
* "room_stats_earliest_token_idx" UNIQUE, btree (room_id)


## Table - room_stats_historical
|        Column        |  Type  | Collation | Nullable | Default |
|----------------------|--------|-----------|----------|---------|
| room_id              | text   |           | not null | |
| end_ts               | bigint |           | not null | |
| bucket_size          | bigint |           | not null | |
| current_state_events | bigint |           | not null | |
| joined_members       | bigint |           | not null | |
| invited_members      | bigint |           | not null | |
| left_members         | bigint |           | not null | |
| banned_members       | bigint |           | not null | |
| local_users_in_room  | bigint |           | not null | |
| total_events         | bigint |           | not null | |
| total_event_bytes    | bigint |           | not null | |

**Indexes**
* "room_stats_historical_pkey" PRIMARY KEY, btree (room_id, end_ts)
* "room_stats_historical_end_ts" btree (end_ts)


## Table - room_stats_state
|       Column       |  Type   | Collation | Nullable | Default |
|--------------------|---------|-----------|----------|---------|
| room_id            | text    |           | not null | |
| name               | text    |           |          | |
| canonical_alias    | text    |           |          | |
| join_rules         | text    |           |          | |
| history_visibility | text    |           |          | |
| encryption         | text    |           |          | |
| avatar             | text    |           |          | |
| guest_access       | text    |           |          | |
| is_federatable     | boolean |           |          | |
| topic              | text    |           |          | |

**Indexes**
* "room_stats_state_room" UNIQUE, btree (room_id)


## Table - room_tags
| Column  | Type | Collation | Nullable | Default |
|---------|------|-----------|----------|---------|
| user_id | text |           | not null | |
| room_id | text |           | not null | |
| tag     | text |           | not null | |
| content | text |           | not null | |

**Indexes**
* "room_tag_uniqueness" UNIQUE CONSTRAINT, btree (user_id, room_id, tag)


## Table - room_tags_revisions
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| user_id   | text   |           | not null | |
| room_id   | text   |           | not null | |
| stream_id | bigint |           | not null | |

**Indexes**
* "room_tag_revisions_uniqueness" UNIQUE CONSTRAINT, btree (user_id, room_id)


## Table - rooms
|    Column    |  Type   | Collation | Nullable | Default |
|--------------|---------|-----------|----------|---------|
| room_id      | text    |           | not null | |
| is_public    | boolean |           |          | |
| creator      | text    |           |          | |
| room_version | text    |           |          | |

**Indexes**
* "rooms_pkey" PRIMARY KEY, btree (room_id)
* "public_room_index" btree (is_public)


## Table - schema_version
|  Column  |     Type     | Collation | Nullable |   Default   |
|----------|--------------|-----------|----------|-------------|
| lock     | character(1) |           | not null | 'X'::bpchar
| version  | integer      |           | not null | |
| upgraded | boolean      |           | not null | |

**Indexes**
* "schema_version_lock_key" UNIQUE CONSTRAINT, btree (lock)

**Check constraints**
* "schema_version_lock_check" CHECK (lock = 'X'::bpchar)


## Table - server_keys_json
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| server_name       | text   |           | not null | |
| key_id            | text   |           | not null | |
| from_server       | text   |           | not null | |
| ts_added_ms       | bigint |           | not null | |
| ts_valid_until_ms | bigint |           | not null | |
| key_json          | bytea  |           | not null | |

**Indexes**
* "server_keys_json_uniqueness" UNIQUE CONSTRAINT, btree (server_name, key_id, from_server)


## Table - server_signature_keys
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| server_name       | text   |           |          | |
| key_id            | text   |           |          | |
| from_server       | text   |           |          | |
| ts_added_ms       | bigint |           |          | |
| verify_key        | bytea  |           |          | |
| ts_valid_until_ms | bigint |           |          | |

**Indexes**
* "server_signature_keys_server_name_key_id_key" UNIQUE CONSTRAINT, btree (server_name, key_id)


## Table - state_events
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| event_id   | text |           | not null | |
| room_id    | text |           | not null | |
| type       | text |           | not null | |
| state_key  | text |           | not null | |
| prev_state | text |           |          | |

**Indexes**
* "state_events_event_id_key" UNIQUE CONSTRAINT, btree (event_id)


## Table - state_group_edges
|      Column      |  Type  | Collation | Nullable | Default |
|------------------|--------|-----------|----------|---------|
| state_group      | bigint |           | not null | |
| prev_state_group | bigint |           | not null | |

**Indexes**
* "state_group_edges_idx" btree (state_group)
* "state_group_edges_prev_idx" btree (prev_state_group)


## Table - state_groups
|  Column  |  Type  | Collation | Nullable | Default |
|----------|--------|-----------|----------|---------|
| id       | bigint |           | not null | |
| room_id  | text   |           | not null | |
| event_id | text   |           | not null | |

**Indexes**
* "state_groups_pkey" PRIMARY KEY, btree (id)
* "state_groups_room_id_idx" btree (room_id)


## Table - state_groups_state
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| state_group | bigint |           | not null | |
| room_id     | text   |           | not null | |
| type        | text   |           | not null | |
| state_key   | text   |           | not null | |
| event_id    | text   |           | not null | |

**Indexes**
* "state_groups_state_type_idx" btree (state_group, type, state_key)


## Table - stats_incremental_position
|  Column   |     Type     | Collation | Nullable |   Default   |
|-----------|--------------|-----------|----------|-------------|
| lock      | character(1) |           | not null | 'X'::bpchar
| stream_id | bigint       |           | not null | |

**Indexes**
* "stats_incremental_position_lock_key" UNIQUE CONSTRAINT, btree (lock)

**Check constraints**
* "stats_incremental_position_lock_check" CHECK (lock = 'X'::bpchar)


## Table - stream_ordering_to_exterm
|     Column      |  Type  | Collation | Nullable | Default |
|-----------------|--------|-----------|----------|---------|
| stream_ordering | bigint |           | not null | |
| room_id         | text   |           | not null | |
| event_id        | text   |           | not null | |

**Indexes**
* "stream_ordering_to_exterm_idx" btree (stream_ordering)
* "stream_ordering_to_exterm_rm_idx" btree (room_id, stream_ordering)


## Table - threepid_guest_access_tokens
|       Column       | Type | Collation | Nullable | Default |
|--------------------|------|-----------|----------|---------|
| medium             | text |           |          | |
| address            | text |           |          | |
| guest_access_token | text |           |          | |
| first_inviter      | text |           |          | |

**Indexes**
* "threepid_guest_access_tokens_index" UNIQUE, btree (medium, address)


## Table - threepid_validation_session
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| session_id        | text   |           | not null | |
| medium            | text   |           | not null | |
| address           | text   |           | not null | |
| client_secret     | text   |           | not null | |
| last_send_attempt | bigint |           | not null | |
| validated_at      | bigint |           |          | |

**Indexes**
* "threepid_validation_session_pkey" PRIMARY KEY, btree (session_id)


## Table - threepid_validation_token
|   Column   |  Type  | Collation | Nullable | Default |
|------------|--------|-----------|----------|---------|
| token      | text   |           | not null | |
| session_id | text   |           | not null | |
| next_link  | text   |           |          | |
| expires    | bigint |           | not null | |

**Indexes**
* "threepid_validation_token_pkey" PRIMARY KEY, btree (token)
* "threepid_validation_token_session_id" btree (session_id)


## Table - ui_auth_sessions
|    Column     |  Type  | Collation | Nullable | Default |
|---------------|--------|-----------|----------|---------|
| session_id    | text   |           | not null | |
| creation_time | bigint |           | not null | |
| serverdict    | text   |           | not null | |
| clientdict    | text   |           | not null | |
| uri           | text   |           | not null | |
| method        | text   |           | not null | |
| description   | text   |           | not null | |

**Indexes**
* "ui_auth_sessions_session_id_key" UNIQUE CONSTRAINT, btree (session_id)

**Referenced by**
* *TABLE "ui_auth_sessions_credentials" CONSTRAINT"ui_auth_sessions_credentials_session_id_fkey" FOREIGN KEY (session_id) REFERENCES ui_auth_sessions(session_id)


## Table - ui_auth_sessions_credentials
|   Column   | Type | Collation | Nullable | Default |
|------------|------|-----------|----------|---------|
| session_id | text |           | not null | |
| stage_type | text |           | not null | |
| result     | text |           | not null | |

**Indexes**
* "ui_auth_sessions_credentials_session_id_stage_type_key" UNIQUE CONSTRAINT, btree (session_id, stage_type)

**Foreign-key constraints**
* "ui_auth_sessions_credentials_session_id_fkey" FOREIGN KEY (session_id) REFERENCES ui_auth_sessions(session_id)


## Table - user_daily_visits
|  Column   |  Type  | Collation | Nullable | Default |
|-----------|--------|-----------|----------|---------|
| user_id   | text   |           | not null | |
| device_id | text   |           |          | |
| timestamp | bigint |           | not null | |

**Indexes**
* "user_daily_visits_ts_idx" btree ("timestamp")
* "user_daily_visits_uts_idx" btree (user_id, "timestamp")


## Table - user_directory
|    Column    | Type | Collation | Nullable | Default |
|--------------|------|-----------|----------|---------|
| user_id      | text |           | not null | |
| room_id      | text |           |          | |
| display_name | text |           |          | |
| avatar_url   | text |           |          | |

**Indexes**
* "user_directory_user_idx" UNIQUE, btree (user_id)
* "user_directory_room_idx" btree (room_id)


## Table - user_directory_search
| Column  |   Type   | Collation | Nullable | Default |
|---------|----------|-----------|----------|---------|
| user_id | text     |           | not null | |
| vector  | tsvector |           |          | |

**Indexes**
* "user_directory_search_user_idx" UNIQUE, btree (user_id)
* "user_directory_search_fts_idx" gin (vector)


## Table - user_directory_stream_pos
|  Column   |     Type     | Collation | Nullable |   Default   |
|-----------|--------------|-----------|----------|-------------|
| lock      | character(1) |           | not null | 'X'::bpchar
| stream_id | bigint       |           |          | |

**Indexes**
* "user_directory_stream_pos_lock_key" UNIQUE CONSTRAINT, btree (lock)

**Check constraints**
* "user_directory_stream_pos_lock_check" CHECK (lock = 'X'::bpchar)


## Table - user_external_ids
|    Column     | Type | Collation | Nullable | Default |
|---------------|------|-----------|----------|---------|
| auth_provider | text |           | not null | |
| external_id   | text |           | not null | |
| user_id       | text |           | not null | |

**Indexes**
* "user_external_ids_auth_provider_external_id_key" UNIQUE CONSTRAINT, btree (auth_provider, external_id)


## Table - user_filters
|   Column    |  Type  | Collation | Nullable | Default |
|-------------|--------|-----------|----------|---------|
| user_id     | text   |           | not null | |
| filter_id   | bigint |           | not null | |
| filter_json | bytea  |           | not null | |

**Indexes**
* "user_filters_unique" UNIQUE, btree (user_id, filter_id)


## Table - user_ips
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| user_id      | text   |           | not null | |
| access_token | text   |           | not null | |
| device_id    | text   |           |          | |
| ip           | text   |           | not null | |
| user_agent   | text   |           | not null | |
| last_seen    | bigint |           | not null | |

**Indexes**
* "user_ips_user_token_ip_unique_index" UNIQUE, btree (user_id, access_token, ip)
* "user_ips_device_id" btree (user_id, device_id, last_seen)
* "user_ips_last_seen" btree (user_id, last_seen)
* "user_ips_last_seen_only" btree (last_seen)


## Table - user_signature_stream
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| stream_id    | bigint |           | not null | |
| from_user_id | text   |           | not null | |
| user_ids     | text   |           | not null | |

**Indexes**
* "user_signature_stream_idx" UNIQUE, btree (stream_id)


## Table - user_stats_current
|          Column           |  Type  | Collation | Nullable | Default |
|---------------------------|--------|-----------|----------|---------|
| user_id                   | text   |           | not null | |
| joined_rooms              | bigint |           | not null | |
| completed_delta_stream_id | bigint |           | not null | |

**Indexes**
* "user_stats_current_pkey" PRIMARY KEY, btree (user_id)


## Table - user_stats_historical
|      Column       |  Type  | Collation | Nullable | Default |
|-------------------|--------|-----------|----------|---------|
| user_id           | text   |           | not null | |
| end_ts            | bigint |           | not null | |
| bucket_size       | bigint |           | not null | |
| joined_rooms      | bigint |           | not null | |
| invites_sent      | bigint |           | not null | |
| rooms_created     | bigint |           | not null | |
| total_events      | bigint |           | not null | |
| total_event_bytes | bigint |           | not null | |

**Indexes**
* "user_stats_historical_pkey" PRIMARY KEY, btree (user_id, end_ts)
* "user_stats_historical_end_ts" btree (end_ts)


## Table - user_threepid_id_server
|  Column   | Type | Collation | Nullable | Default |
|-----------|------|-----------|----------|---------|
| user_id   | text |           | not null | |
| medium    | text |           | not null | |
| address   | text |           | not null | |
| id_server | text |           | not null | |

**Indexes**
* "user_threepid_id_server_idx" UNIQUE, btree (user_id, medium, address, id_server)


## Table - user_threepids
|    Column    |  Type  | Collation | Nullable | Default |
|--------------|--------|-----------|----------|---------|
| user_id      | text   |           | not null | |
| medium       | text   |           | not null | |
| address      | text   |           | not null | |
| validated_at | bigint |           | not null | |
| added_at     | bigint |           | not null | |

**Indexes**
* "medium_address" UNIQUE CONSTRAINT, btree (medium, address)
* "user_threepids_medium_address" btree (medium, address)
* "user_threepids_user_id" btree (user_id)


## Table - users
|           Column           |   Type   | Collation | Nullable | Default |
|----------------------------|----------|-----------|----------|---------|
| name                       | text     |           |          | |
| password_hash              | text     |           |          | |
| creation_ts                | bigint   |           |          | |
| admin                      | smallint |           | not null | 0
| upgrade_ts                 | bigint   |           |          | |
| is_guest                   | smallint |           | not null | 0
| appservice_id              | text     |           |          | |
| consent_version            | text     |           |          | |
| consent_server_notice_sent | text     |           |          | |
| user_type                  | text     |           |          | |
| deactivated                | smallint |           | not null | 0

**Indexes**
* "users_name_key" UNIQUE CONSTRAINT, btree (name)
* "users_creation_ts" btree (creation_ts)


## Table - users_in_public_rooms
| Column  | Type | Collation | Nullable | Default |
|---------|------|-----------|----------|---------|
| user_id | text |           | not null | |
| room_id | text |           | not null | |

**Indexes**
* "users_in_public_rooms_u_idx" UNIQUE, btree (user_id, room_id)
* "users_in_public_rooms_r_idx" btree (room_id)


## Table - users_pending_deactivation
| Column  | Type | Collation | Nullable | Default |
|---------|------|-----------|----------|---------|
| user_id | text |           | not null | |


## Table - users_who_share_private_rooms
|    Column     | Type | Collation | Nullable | Default |
|---------------|------|-----------|----------|---------|
| user_id       | text |           | not null | |
| other_user_id | text |           | not null | |
| room_id       | text |           | not null | |

**Indexes**
* "users_who_share_private_rooms_u_idx" UNIQUE, btree (user_id, other_user_id, room_id)
* "users_who_share_private_rooms_o_idx" btree (other_user_id)
* "users_who_share_private_rooms_r_idx" btree (room_id)


## Sequence - cache_invalidation_stream_seq
|  Type  | Start | Minimum |       Maximum       | Increment | Cycles? | Cache |
|--------|-------|---------|---------------------|-----------|---------|-------|
| bigint |     1 |       1 | 9223372036854775807 |         1 | no      |     1 |


## Sequence - state_group_id_seq
|  Type  | Start | Minimum |       Maximum       | Increment | Cycles? | Cache |
|--------|-------|---------|---------------------|-----------|---------|-------|
| bigint |     1 |       1 | 9223372036854775807 |         1 | no      |     1 |
