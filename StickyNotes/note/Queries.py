QUERY_CREATE_NOTE_ENTRY = """
BEGIN;
INSERT INTO note_entry(title, owner_id) VALUES (\"{title}\", {owner_id});
SELECT LAST_INSERT_ID() INTO @new_note_id;
INSERT INTRO note_text(note_id, text) VALUES (@new_note_id, \"\");
COMMIT;
SELECT @new_note_id AS new_note_id;
"""

QUERY_UPDATE_NOTE = """
BEGIN;
UPDATE note_entry SET change_date=CURRENT_TIMESTAMP WHERE id={note_id} AND owner_id={owner_id};
UPDATE note_text SET text=\"{text}\ WHERE note_id={note_id}";
COMMIT;
"""

QUERY_UPDATE_NOTE_METADATA = 'UPDATE note_entry SET {fields} WHERE id={note_id} AND owner_id={owner_id}'

QUERY_GET_NOTE = 'SELECT * FROM note WHERE id={id} AND owner_id={owner_id} LIMIT 1'

QUERY_GET_NOTES = 'SELECT * FROM note WHERE owner_id={owner_id} ORDER BY id DESC LIMIT {offset},{count}'

QUERY_GET_NOTES_LIST = 'SELECT * FROM note_entry WHERE owner_id={owner_id} ORDER BY id DESC LIMIT {offset},{count}'

QUERY_DELETE_NOTE = 'DELETE FROM note_entry WHERE id={note_id} AND owner_id={owner_id}'
