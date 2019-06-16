from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import time
import os
import pytz

app = Flask(__name__)
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishorder_PS:123456@postgres:5432/dishorder'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:123456@localhost:5432/dishorder'
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/dishorder/uploads'
app.config['TIMEZONE'] = pytz.timezone('Asia/Saigon')
app.config['API_ADDRESS'] = 'http://127.0.0.1:3001/'
app.config['IMG_URI'] = 'img/'
# os.popen('mkdir {}/dishorder/uploads'.format(os.getcwd()))
CORS(app)
while True:
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=True)
        Base = declarative_base()
        from dishorder.views import models

        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        break
    except:
        print('Try to connect to database')
        time.sleep(1)
from dishorder.views.beviews import dishorderapi

app.register_blueprint(dishorderapi)
