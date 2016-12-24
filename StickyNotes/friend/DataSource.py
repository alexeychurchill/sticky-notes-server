from .. import mysql
from ..ResponseCodes import *
from .Query import *

connection = mysql.connect()
cursor = connection.cursor()

def friendCheckIfRequested(userOneId, userTwoId):
    """
    Checks if one of users already requested friendship
    int, int -> bool
    """
    query = QUERY_CHECK_REQUESTED
    query = query.format(**{'user_a_id':userOneId, 'user_b_id':userTwoId})

    cursor.execute(query)
    data = cursor.fetchone()

    if data == None:
        return False

    requestsCount, = data

    return requestsCount > 0


def friendCheckIfFriend(userOneId, userTwoId):
    """
    Checks if users is friends
    int, int -> bool
    """
    query = QUERY_FRIENDSHIP_COUNT
    query = query.format(**{'user_a_id':userOneId, 'user_b_id':userTwoId})

    cursor.execute(query)
    data = cursor.fetchone()

    if data == None:
        return False

    requestsCount, = data

    return requestsCount > 0


def friendMakeRequest(ownerId, userId):
    """
    Makes request for a friendship
    int, int -> bool, int, str
    """
    if friendCheckIfRequested(ownerId, userId):
        return False, ERROR_REQUEST_EXISTS, 'Such friendship request already exists!'

    if friendCheckIfFriend(ownerId, userId):
        return False, ERROR_REQUEST_EXISTS, 'Already friends query = QUERY_MAKE_REQUEST

    query = query.format(**{'requester_id':ownerId, 'user_id':userId})

    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Friendship not requested. Database error.'

    return True, NO_ERROR, 'Friendship requested!'


def friendGetMyRequests(ownerId, page, count):
    """
    Returns user's friendship requests
    int, int, int -> bool, int, str, [{str:int, str:int, str:int,
    str:str, str:str, str:str}]
    """
    query = QUERY_GET_MY_REQUESTS
    query = query.format(**{'owner_id':ownerId, 'offset':(page * count), 'count':count})

    cursor.execute(query)
    data = cursor.fetchone()

    if data == None:
        return False, ERROR_DATABASE, 'Nothing was returned'

    requestList = []

    for friendshipRequest in data:
        id, date, userId, login, name, lastname = friendshipRequest
        mapFriendshipRequest = {'id':id,
                                'date':date,
                                'user_id':userId,
                                'login':login,
                                'name':name,
                                'lastname':lastname}
        requestList.append(mapFriendshipRequest)

    return True, NO_ERROR, 'Success', requestList


def friendGetRequests(ownerId, page = 0, count = 5):
    """
    Returns friendship requests TO user
    int, int, int -> bool, int, str, [{str:int, str:int, str:int,
    str:str, str:str, str:str}]
    """
    query = QUERY_GET_REQUESTS_TO_ME
    query = query.format(**{'owner_id':ownerId, 'offset':(page * count), 'count':count})

    cursor.execute(query)
    data = cursor.fetchone()

    if data == None:
        return False, ERROR_DATABASE, 'Nothing was returned'

    requestList = []

    for friendshipRequest in data:
        id, date, userId, login, name, lastname = friendshipRequest
        mapFriendshipRequest = {'id':id,
                                'date':date,
                                'user_id':userId,
                                'login':login,
                                'name':name,
                                'lastname':lastname}
        requestList.append(mapFriendshipRequest)

    return True, NO_ERROR, 'Success', requestList


def friendAcceptRequest(ownerId, id):
    """
    Accepts request for friendship
    int, int -> bool, int, str
    """
    query = QUERY_ACCEPT_REQUEST
    query = query.format(**{'id':id, 'owner_id':ownerId})

    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Friendship wasn\'t accepted'

    return True, NO_ERROR, 'Friendship accepted'


def friendDeleteRequest(ownerId, id):
    """
    Cancels/rejects request for friendship
    int, int -> bool, int, str
    """
    query = QUERY_DELETE_REQUEST
    query = query.format(**{'id':id, 'owner_id':ownerId})

    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Operation failed!'

    return True, NO_ERROR, 'Successfuly!'


def friendGetFriends(ownerId, page = 0, count = 10):
    """
    Gets list of the friends
    int, int -> bool, int, str, [{str:int, str:str, str:str, str:str}]
    """
    query = QUERY_GET_FRIENDS
    query = query.format(**{'owner_id':ownerId, 'offset':(page * count), 'count':count})

    cursor.execute(query)
    data = cursor.fetchall()

    if data == None:
        return False, ERROR_DATABASE, 'Nothing was returned', None

    friendList = []

    for friendTuple in data:
        id, login, name, lastname = friendTuple
        friendMap = {'id':id, 'login':login, 'name':name, 'lastname':lastname}
        friendList.append(friendMap)

    return True, ERROR_DATABASE, 'Success!', friendList


def friendUnfriend(ownerId, userId):
    """
    Unfriends user
    int, int -> bool, int, str
    """
    try:
        query = QUERY_UNSHARE_ALL_NOTES
        query = query.format(**{'owner_id':ownerId, 'user_id':userId})
        cursor.execute(query)
        query = QUERY_UNFRIEND
        query = query.format(**{'owner_id':ownerId, 'user_id':userId})
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_DATABASE, 'Operation failed!'

    return True, NO_ERROR, 'Unfriend successful!'


