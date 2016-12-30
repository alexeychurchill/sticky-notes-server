from .. import stickyNotes
from .DataSource import *
from ..user.DataSource import userGetIdByAccessToken
from ..ResponseCodes import *
from ..utils.Response import *
from flask import jsonify
from flask import request

@stickyNotes.route('/note/create', methods=['POST'])
def noteCreateRequest():
    """
    Note creation request
    Needs only title
    Returns id of the new note
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    if not 'title' in request.form:
        return jsonify(simpleError(ERROR_NO_DATA, 'You can\'t create note without title'))

    title = request.form['title']
    
    success, resultCode, resultMessage, noteId = noteCreate(id, title)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/note/<int:noteId>', methods=['GET'])
def noteGetRequest(noteId):
    """
    Gets the note by it's id
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, note = noteGet(id, noteId)

    if success:
        return jsonify(response(note))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/note/<int:noteId>/update', methods=['POST'])
def noteUpdateRequest(noteId):
    """
    Updates note
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    if not 'text' in request.form:
        return jsonify(simpleResponse(NO_ERROR, 'Nothing to update'))

    text = request.form['text']

    success, resultCode, resultMessage = noteUpdate(id, noteId, text)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/note/<int:noteId>/update/metadata', methods=['POST'])
def noteUpdateMetadataRequest(noteId):
    """
    Updates note
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    title = ''
    subject = ''

    if 'title' in request.form:
        if request.form['title'] == '':
            title = None
        else:
            title = request.form['title']

    if 'subject' in request.form:
        if request.form['subject'] == '':
            subject = None
        else:
            subject = request.form['subject']

    success, resultCode, resultMessage = noteUpdateMetadata(id, noteId, title, subject)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/note/list/<int:page>', methods=['GET'])
def noteGetListRequest(page):
    """
    Gets list of the user's notes
    One page contains 10 notes
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage, notes = noteList(id, page, 10)

    if success:
        return jsonify(response({
            'notes':notes,
            'count_current':len(notes)
            }))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


@stickyNotes.route('/note/<int:noteId>/delete', methods=['POST'])
def noteDeleteRequest(noteId):
    """
    Deletes note
    """
    if not 'X-AccessToken' in request.headers:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Access token didn\'t provided'))
    
    token = request.headers['X-AccessToken']
    id = userGetIdByAccessToken(token)
    
    if id == -1:
        return jsonify(simpleError(ERROR_UNAUTHORIZED_ACCESS, 'Unauthorized access!'))

    success, resultCode, resultMessage = noteDelete(id, noteId)

    if success:
        return jsonify(simpleResponse(resultCode, resultMessage))
    else:
        return jsonify(simpleError(resultCode, resultMessage))


###
