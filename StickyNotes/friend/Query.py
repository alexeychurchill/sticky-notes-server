QUERY_CHECK_REQUESTED = """
    SELECT
    COUNT(*) AS requests_count
    FROM friend_request 
    WHERE
    (requester_id={user_a_id} AND user_id={user_b_id})
    OR
    (requester_id={user_b_id} AND user_id={user_a_id})
"""

QUERY_FRIENDSHIP_COUNT = """
    SELECT COUNT(*) AS friendship_count
    FROM friend
    WHERE
    (user_a_id={user_a_id} AND user_b_id={user_b_id})
    OR
    (user_a_id={user_b_id} AND user_b_id={user_a_id})
"""

QUERY_MAKE_REQUEST = """
    INSERT INTO
    friend_request(requester_id, user_id)
    VALUES ({requester_id}, {user_id})
"""

QUERY_GET_MY_REQUESTS = """
    SELECT
    friend_request.id AS id,
    UNIX_TIMESTAMP(friend_request.date) AS date,
    user.id AS user_id,
    user.login AS login,
    user.name AS name,
    user.last_name AS lastname
    FROM
    friend_request, user
    WHERE
    friend_request.requester_id={owner_id}
    AND
    user.id=friend_request.user_id
    LIMIT {offset}, {count}
"""

QUERY_GET_REQUESTS_TO_ME = """
    SELECT
    friend_request.id AS id,
    UNIX_TIMESTAMP(friend_request.date) AS date,
    user.id AS user_id,
    user.login AS login,
    user.name AS name,
    user.last_name AS lastname
    FROM
    friend_request, user
    WHERE
    friend_request.user_id={owner_id}
    AND
    user.id=friend_request.requester_id
    LIMIT {offset}, {count}
"""

QUERY_DELETE_REQUEST = """
    DELETE FROM
    friend_request
    WHERE id={id} AND (requester_id={owner_id} OR user_id={owner_id})
"""

QUERY_ACCEPT_REQUEST = """
    BEGIN;
    SELECT requester_id INTO @user_a_id FROM friend_request WHERE id={id} AND (requester_id={owner_id} OR user_id={owner_id});
    SELECT user_id INTO @user_b_id FROM friend_request WHERE id={id} AND (requester_id={owner_id} OR user_id={owner_id});
    INSERT INTO friend(user_a_id, user_b_id) VALUES (@user_a_id, @user_b_id);
    DELETE FROM friend_request WHERE id={id} AND (requester_id={owner_id} OR user_id={owner_id});
    COMMIT;
"""

QUERY_GET_FRIENDS = """
    SELECT
    user.id AS id,
    user.login AS login,
    user.name AS name,
    user.last_name AS lastname
    FROM user, friend
    WHERE
    (friend.user_a_id={owner_id} AND user.id=friend.user_b_id)
    OR
    (friend.user_b_id={owner_id} AND user.id=friend.user_a_id)
    LIMIT {offset}, {count}
"""

QUERY_UNFRIEND = """
    DELETE FROM friend
    WHERE
    (user_a_id={owner_id} AND user_b_id={user_id})
    OR
    (user_a_id={user_id} AND user_b_id={owner_id})
"""

QUERY_UNSHARE_ALL_NOTES = """
    DELETE FROM shared_note
    WHERE
    (user_id={user_id})
    AND
    (note_id IN (SELECT id FROM note WHERE owner_id={owner_id}))
"""

