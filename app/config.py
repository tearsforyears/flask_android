import os

DATABASE = "sqlite:///" + os.path.dirname(__file__) + "/db.sqlite3.db"
UPLOAD = os.path.dirname(os.path.dirname(__file__)) + "/res/"