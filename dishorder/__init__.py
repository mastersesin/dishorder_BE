from flask import Flask, request
from flask_cors import CORS
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.exc import IntegrityError
from sqlalchemy.exc import SQLAlchemyError
from flask_mail import Mail, Message
import time
import os
import pytz
from datetime import datetime
import re

app = Flask(__name__)
# app.config[
#    'SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:ckiuzk4ever@database-2.cjyp0xzhpykc.us-east-2.rds.amazonaws.com:5432/dishorder'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishorder_PS:123456@10.84.128.31:5430/dishorder'
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
app.config['ALLOWED_EXTENSIONS'] = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
app.config['UPLOAD_FOLDER'] = os.getcwd() + '/dishorder/uploads'
app.config['TIMESTAMP_START'] = int(datetime.now(pytz.timezone('Asia/Saigon')).timestamp())
app.config['API_ADDRESS'] = 'http://10.84.128.31:5000/'
app.config['IMG_URI'] = 'img/'
app.config['VALID_INPUT_STRING_REGEX_COMPILED'] = re.compile('^[a-zA-Z0-9]+[a-zA-Z0-9]$')
# os.popen('mkdir {}/dishorder/uploads'.format(os.getcwd()))
app.config['MAIL_SERVER'] = '10.84.128.25'
app.config['MAIL_PORT'] = 25
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = False
app.config['MAIL_DEFAULT_SENDER'] = "DI Ltd. Reception<reception@diltd.com.vn>"
a = 1
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
        mail = Mail(app)
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
