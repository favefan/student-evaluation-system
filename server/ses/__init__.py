from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from ses import config

db = SQLAlchemy()
migrate = Migrate()

app = Flask(__name__, instance_relative_config=True)
app.config.from_object(config)

db.init_app(app)
migrate.init_app(app, db)

from ses.routes import *
