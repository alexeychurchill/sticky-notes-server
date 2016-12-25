from .. import mysql
from .Queries import *
from ..ResponseCodes import *

connection = mysql.connect()
cursor = connection.cursor()

def sharedShare(ownerId, userId, noteId, editPermission):
    """
    Shares note to another user
    int, int, int, int -> bool, int, str
    """
    query = QUERY_SHARE
    query = query.format(**{'owner_id':ownerId,
                            'note_id':noteId,
                            'user_id':userId,
                            'edit_permission':editPermission
                            })
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Failed to share note!'

    return True, NO_ERROR, 'Note shared!'


def sharedUnshare(ownerId, sharingId):
    """
    Cancels sharing note to the user
    int, int -> bool, int, str
    """
    query = QUERY_UNSHARE
    query = query.format(**{'owner_id':ownerId, 'sharing_id':sharingId})
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Failed to unshare note!'

    return True, NO_ERROR, 'Unshared!'


def sharedList(myId, page = 0, count = 10):
    """
    Gets notes which shared to user
    int, int, int -> bool, int, str, [{str:int, str:str, str:str, str:int,
    str:int, str:str, str:str, str:str}]
    """
    query = QUERY_SHARED_TO_ME
    query = query.format(**{'my_id':myId,
                            'offset':(page * count),
                            'count':count})
    cursor.execute(query)
    data = cursor.fetchall()
    if data == None:
        return False, ERROR_DATABASE, 'Nothing was returned', None

    sharedList = []

    for sharedTuple in data:
        noteId, title, subject, changeDate, ownerId, ownerLogin, ownerName, ownerLastname = sharedTuple
        sharedMap = {'note_id':noteId,
                     'title':title,
                     'subject':subject,
                     'change_date':changeDate,
                     'owner_id':ownerId,
                     'owner_login':ownerLogin,
                     'owner_name':ownerName,
                     'owner_lastname':ownerLastname}
        sharedList.append(sharedMap)

    return True, NO_ERROR, 'Success!', sharedList


def sharedToList(ownerId, noteId, page = 0, count = 10):
    """
    Gets users which note was shared to
    int, int, int, int -> bool, int, str, [{str:int, str:str, str:str, str:int}]
    """
    query = QUERY_SHARED_TO
    query = query.format(**{'owner_id':ownerId,
                            'note_id':noteId,
                            'offset':(page * count),
                            'count':count})
    cursor.execute(query)
    data = cursor.fetchall()
    if data == None:
        return False, ERROR_DATABASE, 'Nothing was returned', None

    sharedToList = []

    for sharedToTuple in data:
        id, login, name, lastname = sharedToTuple
        sharedToMap = {'id':id,
                       'login':login,
                       'name':name,
                       'lastname':lastname}
        sharedToList.append(sharedToMap)

    return True, NO_ERROR, 'Success!', sharedToList
    

def sharedGet(ownerId, noteId):
    """
    Gets shared to user ownerId note with noteId
    int, int -> bool, int, str, {str:int,
    str:str, str:str, str:str,
    str:int, str:int, str:int}
    """
    query = QUERY_SHARED_GET
    query = query.format(**{'owner_id':ownerId, 'note_id':noteId})

    cursor.execute(query)
    data = cursor.fetchone()

    if data == None:
        return False, ERROR_DATABASE, 'Nothing was returned!', None

    id, title, subject, text, changeDate, ownerId, editPermission = data

    return True, NO_ERROR, 'Success!', {'id':id,
                                        'title':title,
                                        'subject':subject,
                                        'text':text,
                                        'change_date':changeDate,
                                        'owner_id':ownerId,
                                        'edit_permission':editPermission}

def sharedCanUpdate(ownerId, noteId):
    """
    Shared can update
    int, int -> bool, bool
    """
    query = QUERY_SHARED_CAN_UPDATE
    query = query.format(**{'owner_id':ownerId, 'note_id':noteId})
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return False, False
    canEdit, = data
    if canEdit == 1:
        return True, True
    return True, False

def sharedUpdate(ownerId, noteId, text):
    """
    Updates shared note
    int, int, str -> bool, int, str
    """
    isExist, isCanEdit = sharedCanUpdate(ownerId, noteId)
    if isExist == False:
        return False, ERROR_DATABASE, 'Sharing doesn\'t exist!'
    if isCanEdit == False:
        return False, ERROR_DATABASE, 'You can\'t edit this!'
    query = QUERY_SHARED_UPDATE
    query = query.format(**{'note_id':noteId, 'text':text})
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Shared update fail!'
    return True, ERROR_DATABASE, 'Shared updated!'


