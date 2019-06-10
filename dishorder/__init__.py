from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy
import psycopg2
import time

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishorder_PS:123456@postgres:5432/dishorder'
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
CORS(app)
db = SQLAlchemy(app)

from dishorder.views.beviews import dishorderapi

app.register_blueprint(dishorderapi)
while True:
    try:
        db.create_all()
        db.session.commit()
        break
    except:
        time.sleep(1)
