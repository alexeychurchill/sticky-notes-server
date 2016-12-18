from . import stickyNotes
from . import mysql

from flask import jsonify
from flask import request
from StickyNotes.utils.Response import response, simpleError

@stickyNotes.route('/user/register', methods=['POST'])
def userRegister():
    if request.method != 'POST':
        return simpleError(1, 'Unsupported method')
    
    
    return "1"

