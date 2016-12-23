from . import stickyNotes
from . import mysql
from StickyNotes.UserDataSource import *
from .ResponseCodes import *

from flask import jsonify
from flask import request
from StickyNotes.utils.Response import response, simpleError, simpleResponse

@stickyNotes.route('/user/register', methods=['POST'])
def userRegisterRequest():
    """
    Request for user registration
    No access_token needed
    """
    login = request.form['login']
    password = request.form['password']
    success, code, message = userRegister(login, password)
    if success:
        return jsonify(simpleResponse(code, message))
    else:
        return jsonify(simpleError(code, message))


@stickyNotes.route('/user/login', methods=['POST'])
def userLoginRequest():
    """
    Request for user login
    Returns access_token
    """
    login = request.form['login']
    password = request.form['password']

    success, code, message = userLogin(login, password)

    if success:
        return jsonify(response({'access_token':message}))
    else:
        return jsonify(simpleError(code, message))


@stickyNotes.route('/user', methods=['GET'])
def userRequest():
    """
    Request for current user
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))
    success, userId, login, name, lastName = userById(id)
    if success:
        return jsonify(response({'user':{'id':userId, 'login':login, 'name':name, 'last_name':lastName}}))
    else:
        return jsonify(simpleError(ERROR_SOME_MYSTERY, 'Some mystery error occured'))


def representsInt(s):
    try: 
        int(s)
        return True
    except ValueError:
        return False


@stickyNotes.route('/user/<userIdLogin>', methods=['GET'])
def userByIdRequest(userIdLogin):
    """
    Request for user by id or login
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    userTuple = ()

    if representsInt(userIdLogin):
        userTuple = userById(int(userIdLogin))
    else:
        userTuple = userByLogin(userIdLogin)
    
    success, userId, login, name, lastName = userTuple

    if success:
        return jsonify(response({'user':{'id':userId, 'login':login, 'name':name, 'last_name':lastName}}))
    else:
        return jsonify(simpleError(login, 'No such user'))


@stickyNotes.route('/user', methods=['POST'])
def userChangedRequest():
    """
    Request for setting name and lastname for a user.
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthoridzed access!'))

    name = ''
    lastname = ''

    if 'name' in request.form:
        if request.form['name'] == '':
            name = None
        else:
            name = request.form['name']

    if 'lastname' in request.form:
        if request.form['lastname'] == '':
            lastname = None
        else:
            lastname = request.form['lastname']

    success, code, message = userUpdate(id, name, lastname)

    if success:
        return jsonify(simpleResponse(code, message))
    else:
        return jsonify(simpleError(code, message))


@stickyNotes.route('/user/search', methods=['POST'])
def userSearchRequest():
    """
    Request for searching users by their nickname
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthoridzed access!'))

    if not 'query' in request.form:
        return jsonify(simpleError(ERROR_NO_DATA, 'No query provided'))

    query = request.form['query']

    success, users = userSearch(query)

    return jsonify(response({'users':users}))


    

