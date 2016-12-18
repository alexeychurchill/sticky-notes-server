from . import stickyNotes
from flask import jsonify
from flask import request
from werkzeug.exceptions import *
from StickyNotes.utils.Response import response, simpleError

@stickyNotes.errorhandler(BadRequest)
def handlerBadRequest(e):
    return jsonify(simpleError(400, 'Bad request'))

@stickyNotes.errorhandler(MethodNotAllowed)
def handlerMethodNotAllowed(e):
    return jsonify(simpleError(405, 'Method Not Allowed'))

@stickyNotes.errorhandler(NotFound)
def handlerMethodNotAllowed(e):
    return jsonify(simpleError(404, 'Not Found'))

@stickyNotes.errorhandler(InternalServerError)
def handlerMethodNotAllowed(e):
    return jsonify(simpleError(500, 'Internal Server Error'))
