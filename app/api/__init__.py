from flask import Flask
from os import environ as env

# Init app
app = Flask(__name__)

import api.routes

app.config['SQLALCHEMY_DATABASE_URI'] = env.get("SQLALCHEMY_DATABASE_URI")
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = env.get("SQLALCHEMY_TRACK_MODIFICATIONS")
app.secret_key = env.get("APP_SECRET_KEY")

from .models import Raw_data, Geoip , db, raw_data_schema, raw_datas_schema

# Database
with app.app_context():
        db.init_app(app)
        db.create_all()
