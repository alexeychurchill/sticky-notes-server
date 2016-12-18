from . import stickyNotes

from flask import jsonify
from StickyNotes.utils.Response import response, simpleError

@stickyNotes.route('/')
def user():
    err = simpleError(10, "Some message")
    return jsonify(err)

