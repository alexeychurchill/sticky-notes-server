from . import stickyNotes
from . import mysql

def isUserExists(login):
    cursor = mysql.connect().cursor()
    query = 'SELECT * FROM '
