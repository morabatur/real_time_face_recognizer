from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_marshmallow import Marshmallow
import os

app = Flask(__name__)
basedir = os.path.abspath(os.path.dirname(__file__))
# Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'mssql+pyodbc://py:py@127.0.0.1:1436/db_py?driver=SQL+Server+Native+Client+11.0'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Init
db = SQLAlchemy(app)

# init ma
ma = Marshmallow(app)


