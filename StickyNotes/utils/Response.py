def response(body):
    return {'type':'response',
            'response':body}

def simpleResponse(code, message):
    """
    Simple response with message and code
    """
    return response({'code':code, 'message':message})

def error(body):
    """
    Returns error. Can be used for returning complex error
    """
    return {'type':'error',
            'error':body}

def simpleError(code, message):
    """
    Returns simple error: error with code and message
    """
    return error({'code':code, 'message':message})
