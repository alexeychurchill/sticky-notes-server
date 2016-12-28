from .. import stickyNotes
from .. import mysql
from .DataSource import *
from ..ResponseCodes import *
from ..user.DataSource import userGetIdByAccessToken
from flask import jsonify
from flask import request
from ..utils.Response import response, simpleError, simpleResponse

@stickyNotes.route('/friend/request/make/<int:userId>', methods=['POST'])
def friendMakeRequestRequest(userId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage = friendMakeRequest(id, userId)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/friend/requests/my/<int:page>', methods=['GET'])
def friendGetMyRequestsRequest(page):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, requests = friendGetMyRequests(id, page)

    if success:
        return jsonify(response(requests))
    else:
        return jsonify(simpleError(resultCode, resultMessage))




@stickyNotes.route('/friend/requests/<int:page>', methods=['GET'])
def friendGetRequestsRequest(page):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, requests = friendGetRequests(id, page)

    if success:
        return jsonify(response(requests))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/friend/request/<int:requestId>/accept', methods=['POST'])
def friendAcceptRequestRequest(requestId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage = friendAcceptRequest(id, requestId)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/friend/request/<int:requestId>/delete', methods=['POST'])
def friendDeleteRequestRequest(requestId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage = friendDeleteRequest(id, requestId)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/friend/list/<int:page>', methods=['GET'])
def friendGetFriendsRequest(page):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, friends = friendGetFriends(id, page)

    if success:
        return jsonify(response(friends))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/friend/<int:userId>/unfriend', methods=['POST'])
def friendUnfriendRequest(userId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage = friendUnfriend(id, userId)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))
