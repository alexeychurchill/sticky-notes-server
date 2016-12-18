from . import stickyNotes
from . import mysql
from StickyNotes.UserDataSource import *

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
    if (userExists(login)):
        return jsonify(simpleError(1, 'User already exists'))
    if (userRegister(login, password) == False):
        return jsonify(simpleError(1, 'Registration failed'))
    return jsonify(simpleResponse(0, 'Registration success:)'))

@stickyNotes.route('/user/login', methods=['POST'])
def userLoginRequest():
    """
    Request for user login
    Returns access_token
    """
    login = request.form['login']
    password = request.form['password']
    return jsonify(simpleResponse(0, userGetId(login, password)))
