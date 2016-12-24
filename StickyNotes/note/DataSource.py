from .. import mysql
from .Queries import *
from ..ResponseCodes import *

connection = mysql.connect()
cursor = connection.cursor()

def noteCreate(ownerId, title):
    """
    Creates note
    int, str -> bool, int, string, int
    """
    query = QUERY_CREATE_NOTE_ENTRY
    query = query.format(**{'owner_id':ownerId, 'title':title})
    data = None
    try:
        cursor.execute(query)
        connection.commit()
        data = cursor.fetchone()
    except Exception as e:
        return False, ERROR_CREATION_NOTE, 'Error creating note', -1
    noteId = -1
    if data != None:
        noteId, = data
    return True, NO_ERROR, 'Note created', noteId


def noteUpdate(ownerId, noteId, text):
    """
    Updates note
    int, int, str -> bool, int, str
    """
    query = QUERY_UPDATE_NOTE
    query = query.format(**{'owner_id':ownerId, 'note_id':noteId, 'text':text})

    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_UPDATE_NOTE, 'Note update failed'

    return True, NO_ERROR, 'Success'


def noteUpdateMetadata(ownerId, noteId, title = '', subject = ''):
    """
    Can updates note's title and subject
    int, int, str, str -> bool, int, str
    """

    if title == '' and subject == '':
        return True, NO_ERROR, 'Nothing was changed'

    query = QUERY_UPDATE_NOTE_METADATA
    queryFields = ''
    if title != '':
        queryFields += 'title="' + title + '"'

    if subject != '':
        if queryFields != '':
            queryFields += ', '
        queryFields += 'subject="' + subject + '"'

    query = query.format(**{'owner_id':ownerId, 'note_id':noteId, 'fields':queryFields})
    
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, NO_ERROR, 'Note update failed'

    return True, NO_ERROR, 'Success'


def noteGet(ownerId, noteId):
    """
    Gets note
    int, int -> bool, int, str, {str:int, str:str, str:str, str:str,
    str:int, str:int, str:int}
    """

    query = QUERY_GET_NOTE
    query = query.format(**{'id':noteId, 'owner_id':ownerId})

    cursor.execute(query)

    data = cursor.fetchone()

    if data == None:
        return False, ERROR_GETTING_NOTE, 'Error getting note', None

    id, title, subject, text, creationDate, changeDate, ownerId = data

    return True, NO_ERROR, '', {
        'id':id,
        'title':title,
        'subject':subject,
        'text':text,
        'creation_date':creationDate,
        'change_date':changeDate,
        'owner_id':ownerId
        }


def noteList(ownerId, page = 0, count = 15):
    """
    Gets notes list
    Returns only entries
    int, int, int -> bool, int, str, [{str:int,
    str:str, str:str,
    str:int, str:int,
    str:int}]
    """

    query = QUERY_GET_NOTES_LIST
    query = query.format(**{'owner_id':ownerId, 'offset':(page * count), 'count':count})

    cursor.execute(query)
    data = cursor.fetchall()

    if data == None:
        return False, ERROR_GETTING_NOTES_LIST, 'Failed', None

    notesList = []

    for noteTuple in data:
        id, title, subject, creationDate, changeDate, ownerId = noteTuple
        noteDict = {
            'id':id,
            'title':title,
            'subject':subject,
            'creation_date':creationDate,
            'change_date':changeDate,
            'owner_id':ownerId
            }
        notesList.append(noteDict)

    return True, NO_ERROR, '', notesList


def noteDelete(ownerId, noteId):
    """
    Deletes note
    int, int -> bool, int, str
    """
    query = QUERY_DELETE_NOTE
    query = query.format(**{'owner_id':ownerId, 'note_id':noteId})

    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DELETING_NOTE, 'Note deleting error'

    return True, NO_ERROR, 'Deleted successfuly!'




    
