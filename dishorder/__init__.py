from flask import Flask
from flask_cors import CORS
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dishorder_PS:123456@localhost:5430/dishorder'
app.config['SECRET_KEY'] = 'trantrongtyckiuzk4ever!@#!!!@@##!*&%^$$#$'
db = SQLAlchemy(app)
from dishorder.views.beviews import dishorderapi
app.register_blueprint(dishorderapi)
db.create_all()
