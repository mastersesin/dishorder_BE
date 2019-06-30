from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
import time
import os
import pytz
from datetime import datetime
import re

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishorder_PS:123456@postgres:5432/dishorder'
# app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishorder_PS:123456@localhost:5430/dishorder'
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/dishorder/uploads'
app.config['TIMESTAMP_START'] = int(datetime.now(pytz.timezone('Asia/Saigon')).timestamp())
app.config['API_ADDRESS'] = 'http://127.0.0.1:3001/'
app.config['IMG_URI'] = 'img/'
app.config['VALID_INPUT_STRING_REGEX_COMPILED'] = re.compile('^[a-zA-Z0-9]+[a-zA-Z0-9]$')
# os.popen('mkdir {}/dishorder/uploads'.format(os.getcwd()))
CORS(app)
while True:
    try:
        engine = create_engine(app.config['SQLALCHEMY_DATABASE_URI'], echo=False)
        Base = declarative_base()
        from dishorder.views import models

        Base.metadata.create_all(engine)
        Session = sessionmaker()
        Session.configure(bind=engine)
        session = Session()
        break
    except SQLAlchemyError as ex:
        print(ex)
        print('Try to connect to database')
        time.sleep(1)
from dishorder.views.beviews import dishorderapi

try:
    default_photo = models.Photos(photo_type='default', type_id=0, path='insert-picture-icon.png')
    session.add(default_photo)
    session.commit()
except IntegrityError as ex:
    # import sys
    # import re
    # print(re.findall(r'\"(.+)\"', str(ex.args)), file=sys.stderr)
    session.rollback()
app.register_blueprint(dishorderapi)
