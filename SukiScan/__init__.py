from flask import Flask
from flask_migrate import Migrate
from flask_sqlalchemy import SQLAlchemy
from SukiScan import config

app = Flask(__name__)
app.secret_key = "SukiScan"
app.config.from_object(config)
db = SQLAlchemy(app)
migrate = Migrate(app, db)

from SukiScan import route
from SukiScan import forms
from SukiScan import models 