from . import stickyNotes
from . import mysql
from StickyNotes.UserDataSource import userRegister, userLogin, userGetIdByAccessToken, userById, userByLogin
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
    Request for user by id
    """
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

