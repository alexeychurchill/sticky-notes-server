from . import stickyNotes
from . import mysql
from .ResponseCodes import *
from .UserQueries import *
import hashlib
import random

connection = mysql.connect()
cursor = connection.cursor()

def md5Hash(source):
    md5hasher = hashlib.md5()
    md5hasher.update(source.encode('utf8'))
    return md5hasher.hexdigest()

def userByQuery(query):
    """
    Returns user by query
    int -> bool, int, str, str, str
    """
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return False, -1, ERROR_NO_SUCH_USER, '', ''
    id, login, name, last_name = data
    return True, id, login, name, last_name
    

def userByLogin(login):
    """
    Gets user by his login if exists
    int -> bool, int, str, str, str
    """
    query = QUERY_GET_USER_BY_LOGIN
    query = query.format(**{'login':login})
    return userByQuery(query)


def userById(id):
    """
    Gets user by his id if exists
    int -> bool, int, str, str, str
    """
    query = QUERY_GET_USER_BY_ID
    query = query.format(**{'id':id})
    return userByQuery(query)


def userGetAccessToken(id):
    """
    Returns access token by user's id if exists
    int -> str
    """
    query = QUERY_GET_USER_TOKEN
    query = query.format(**{'id':id})
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return ''
    accessToken, = data
    return accessToken


def userGetIdByAccessToken(token):
    """
    Gets user's id by his access token if exists
    str -> int
    """
    query = QUERY_GET_USER_ID_BY_TOKEN
    query = query.format(**{'access_token':token})
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return -1
    id, = data
    return id


def generateHexHash():
    """
    Generates random long hex number string (MD5(random number as string))
    () -> str
    """
    randomStr = str(random.randint(1, 20000000000))
    return md5Hash(randomStr)


def userGenerateAccessToken(id):
    """
    Generates user's access token by his id
    int -> str
    """
    possibleToken = ''
    proceed = True
    while (proceed):
        possibleToken = generateHexHash()
        occupied_id = userGetIdByAccessToken(possibleToken)
        if occupied_id == -1:
            proceed = False
    query = QUERY_SET_USER_TOKEN
    query = query.format(**{'id':id, 'token':possibleToken})
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return ''
    return possibleToken


def userLogin(login, password):
    """
    Logins user and returns access token
    str, str -> bool, int, str
    """
    query = QUERY_GET_USER_ID_BY_CREDENTIALS
    passwordHash = md5Hash(password)
    query = query.format(**{'login':login, 'password':passwordHash})
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return False, ERROR_LOGIN_FAILED, 'No such user!'
    id, = data
    token = userGetAccessToken(id)
    if token == '':
        token = userGenerateAccessToken(id)
    if token == '':
        return False, ERROR_TOKEN_GENERATION, 'Error token generation!'
    return True, NO_ERROR, token


def userRegister(login, password):
    """
    Registers user with specified login and password
    str, str -> bool, int, str
    """
    result, id, exist_login, exist_name, exist_last_name = userByLogin(login)
    if result:
        return False, ERROR_REGISTRATION_EXISTS, 'User already exists'
    query = QUERY_INSERT_USER
    passwordHash = md5Hash(password)
    query = query.format(**{'login':login, 'password':passwordHash})
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_REGISTRATION_FAILED, 'Failed user adding'
    return True, NO_ERROR, 'Registrarion successful!'
    

def userUpdate(id, name='', lastname=''):
    """
    Updates user's name and lastname.
    If you need to unset name or lastname they must equal None.
    int, str, str -> bool, int, str
    """
    if name == '' and lastname == '':
        return True, NO_ERROR, 'No one changed'
    queryFields = ''
    if name != '':
        if name == None:
            queryFields = 'name=null'
        else:
            queryFields = 'name="' + name + '"'
    if lastname != '':
        if queryFields != '':
            queryFields += ', '
        if lastname == None:
            queryFields += 'last_name=null'
        else:
            queryFields += 'last_name="' + lastname + '"'
    query = QUERY_UPDATE_USER
    query = query.format(**{'fields':queryFields, 'id':id})

    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False, ERROR_SOME_MYSTERY, 'Some mystery error was occured'
    
    return True, NO_ERROR, 'Success!'


def userSearch(loginQuery):
    """
    Performs search in users' logins
    str -> bool, [{str:int, str:str, str:str, str:str}]
    """
    if loginQuery == '':
        return True, []
    query = QUERY_SEARCH_USER
    query = query.format(**{'query':loginQuery})

    cursor.execute(query)

    data = cursor.fetchall()

    userList = []
    for userTuple in data:
        id, login, name, lastname = userTuple
        userList.append({'id':id, 'login':login, 'name':name, 'lastname':lastname})

    return True, userList



    

    
