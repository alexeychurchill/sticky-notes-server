from .. import stickyNotes
from .DataSource import *
from ..user.DataSource import userGetIdByAccessToken
from ..ResponseCodes import *
from ..utils.Response import *
from flask import jsonify
from flask import request

@stickyNotes.route('/shared/share', methods=['POST'])
def sharedShareRequest():
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    if not 'note_id' in request.form:
        return jsonify(simpleError(ERROR_NO_DATA, 'You need to specify id of the note you want share'))
    
    noteId = request.form['note_id']

    if not 'edit_permission' in request.form:
        return jsonify(simpleError(ERROR_NO_DATA, 'You need to specify edit permission'))

    editPermission = request.form['edit_permission']

    if not 'user_id' in request.form:
        return jsonify(simpleError(ERROR_NO_DATA, 'You need to specify id of the user'))
    
    userId = request.form['user_id']

    success, resultCode, resultMessage = sharedShare(id, userId, noteId, editPermission)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/shared/sharing/<int:sharingId>/unshare', methods=['POST'])
def sharedUnshareRequest(sharingId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage = sharedUnshare(id, sharingId)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/shared/list/<int:page>', methods=['GET'])
def sharedListRequest(page):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, notes = sharedList(id, page)

    if success:
        return jsonify(response({'notes':notes}))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/shared/<int:noteId>/to/<int:page>', methods=['GET'])
def sharedToListRequest(noteId, page):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, users = sharedToList(id, noteId, page)

    if success:
        return jsonify(response({'users':users}))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/shared/<int:noteId>', methods=['GET'])
def sharedGetRequest(noteId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, sharedNote = sharedGet(id, noteId)

    if success:
        return jsonify(response(sharedNote))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/shared/<int:noteId>/update', methods=['POST'])
def sharedUpdateRequest(noteId):
    """
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    if not 'text' in request.form:
        return jsonify(simpleError(ERROR_NO_DATA, 'You need to specify new text'))
    
    text = request.form['text']
    
    success, resultCode, resultMessage = sharedUpdate(id, noteId, text)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))
