from flask import Flask

stickyNotes = Flask(__name__)

from . import User
