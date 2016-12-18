def response(body):
    return {"response":body}

def error(body):
    """
    Returns error. Can be used for returning complex error
    """
    return {"error":body}

def simpleError(code, message):
    """
    Returns simple error: error with code and message
    """
    return error({"code":code, "message":message})
