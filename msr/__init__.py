from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager

app = Flask(__name__)

data_base = 'msr.db'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + data_base
app.config['SECRET_KEY'] = 'ec9439cfc6c796ae2029594d'

db = SQLAlchemy(app)

my_bcrypt = Bcrypt(app)

login_manager = LoginManager(app)
login_manager.login_view = "login_page"
login_manager.login_message_category = "info"

from msr import main
from msr import authentication