from flask import Flask
from flaskext.mysql import MySQL

from . import Config

mysql = MySQL()
stickyNotes = Flask(__name__)
stickyNotes.config['MYSQL_DATABASE_USER'] = Config.USER
stickyNotes.config['MYSQL_DATABASE_PASSWORD'] = Config.PASSWORD
stickyNotes.config['MYSQL_DATABASE_DB'] = Config.DATABASE
stickyNotes.config['MYSQL_DATABASE_HOST'] = Config.HOST
mysql.init_app(stickyNotes)

from . import User
