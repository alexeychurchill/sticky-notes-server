from . import stickyNotes

@stickyNotes.route('/')
def user():
    return 'user'

