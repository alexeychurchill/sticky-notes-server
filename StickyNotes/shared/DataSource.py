from .. import mysql
from .Queries import *
from ..ResponseCodes import *

connection = mysql.connect()
cursor = connection.cursor()

