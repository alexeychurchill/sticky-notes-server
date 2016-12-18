from . import stickyNotes
from . import mysql
import hashlib

def md5Hash(source):
    md5hasher = hashlib.md5()
    md5hasher.update(source.encode('utf8'))
    return md5hasher.hexdigest()

def userLoginCount(login):
    """
    Returns count of users with specified login.
    Normally will return 0 or 1
    """
    cursor = mysql.connect().cursor()
    query = 'SELECT COUNT(*) AS userCount FROM user WHERE login="{login}"'
    queryParams = {'login':login}
    query = query.format(**queryParams)
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return 0
    return data[0]

def userExists(login):
    """
    Checks if user with specified login exists
    """
    return userLoginCount(login) > 0

def userRegister(login, password):
    """
    Registers user with specified login and password
    """
    if userExists(login) == True:
        return False
    connection = mysql.connect()
    cursor = connection.cursor()
    query = 'INSERT INTO user(login, password) VALUES ("{login}", "{password}")'
    md5hasher = hashlib.md5()
    md5hasher.update(password.encode('utf8'))
    passwordHash = md5hasher.hexdigest()
    query = query.format(**{'login':login, 'password':passwordHash})
    try:
        cursor.execute(query)
        connection.commit()
    except Exception as e:
        return False
    return True

def accessTokenExists(accessToken):
    """
    Checks if such access token exists
    """
    cursor = mysql.connect().cursor()
    query = 'SELECT COUNT(*) AS count FROM access_token WHERE access_token="{token}"'
    query = query.format(**{'token':accessToken})
    cursor.execute(query)
    data = cursor.fetchone()
    return data[0] > 0

def userGetId(login, password):
    """
    Get user id from login and password
    """
    cursor = mysql.connect().cursor()
    passwordHash = md5Hash(password)
    query = 'SELECT id FROM user WHERE login="{login}" AND password="{password}"'
    query = query.format(**{'login':login, 'password':passwordHash})
    cursor.execute(query)
    data = cursor.fetchone()
    if data == None:
        return -1
    return data[0]

def userLogin(login, password):
    """
    Logins user and returns access token
    """
    if (userExists(login) == False):
        return ''

    
