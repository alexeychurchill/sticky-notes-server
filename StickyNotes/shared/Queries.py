QUERY_SHARE = """
    INSERT INTO
    shared_note(note_id, user_id, edit_permission)
    SELECT
    note.id, {user_id}, {edit_permission}
    FROM
    note
    WHERE
    note.id={note_id} AND note.owner_id={owner_id}
"""

QUERY_UNSHARE = """
    DELETE FROM shared_note
    WHERE
    id={sharing_id}
    AND
    note_id IN (SELECT id FROM note WHERE owner_id={owner_id})
"""

QUERY_SHARED_TO_ME = """
    SELECT
    note.id AS note_id,
    note.title AS title,
    note.subject AS subject,
    UNIX_TIMESTAMP(note.change_date) AS change_date,
    user.id AS owner_id,
    user.login AS owner_login,
    user.name AS owner_name,
    user.last_name AS owner_lastname
    FROM
    shared_note, note, user
    WHERE
    user.id=note.owner_id
    AND
    note.id=shared_note.note_id
    AND
    shared_note.user_id={my_id}
    LIMIT {offset},{count}
"""

QUERY_SHARED_TO = """
    SELECT
    user.id AS id,
    user.login AS login,
    user.name AS name,
    user.last_name AS lastname
    FROM
    user, shared_note
    WHERE
    shared_note.note_id={note_id}
    AND
    user.id=shared_note.user_id
    AND
    note_id IN (SELECT id FROM note WHERE owner_id={owner_id})
    LIMIT {offset},{count}
"""
    
QUERY_SHARED_GET = """
    SELECT
    note.id AS id,
    note.title AS title,
    note.subject AS subject,
    note.text AS text,
    UNIX_TIMESTAMP(note.change_date) AS change_date,
    note.owner_id AS owner_id,
    shared_note.edit_permission AS edit_permission
    FROM
    note, shared_note
    WHERE
    note.id=shared_note.note_id
    AND
    shared_note.note_id={note_id}
    AND
    shared_note.user_id={owner_id}
"""

QUERY_SHARED_CAN_UPDATE = """
    SELECT
    edit_permission
    FROM
    shared_note
    WHERE
    note_id={note_id}
    AND
    user_id={owner_id}
    LIMIT 1
"""

QUERY_SHARED_UPDATE = """
    UPDATE
    note
    SET
    text={text}
    WHERE
    id={note_id}
"""
