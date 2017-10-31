from flask import Flask
from flask_login import LoginManager
#from flask_debugtoolbar import DebugToolbarExtension
from flask_migrate import Migrate
import shekels.logger
from shekels.db_sqlalchemy import db


shekels.logger.setup()

app = Flask(__name__)
app.secret_key = 'fdsafhsdalkghsdahg'
app.debug = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql+psycopg2://marstom_shekels:marstom_shekels@188.40.77.144/marstom_shekels'
#app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False



#toolbar = DebugToolbarExtension(app)

db.init_app(app)
migrate = Migrate(app, db)

import shekels.views
import shekels.models
