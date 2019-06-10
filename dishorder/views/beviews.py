from flask import request, jsonify, Blueprint, abort, flash, request, redirect, url_for
from .functions import *
from .return_msg import ReturnMSG
from dishorder import session
from .models import *
import calendar
import pytz
from datetime import datetime
import sys
from werkzeug.utils import secure_filename
import os

dishorderapi = Blueprint('dishorderapi', __name__)
tz = pytz.timezone('Asia/Saigon')


@dishorderapi.route('/upload', methods=['POST'])
def upload():
    print(request.files, file=sys.stderr)
    # check if the post request has the file part
    if 'file' not in request.files:
        msg = ReturnMSG().no_file_part
        return jsonify(msg)
    file = request.files['file']
    # if user does not select file, browser also
    # submit a empty part without filename
    if file.filename == '':
        msg = ReturnMSG().no_selected_file
        return jsonify(msg)
    if file and allowed_file(file.filename):
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        msg = ReturnMSG().upload_successfully
        return jsonify(msg)


@dishorderapi.route('/test', methods=['GET'])
def test():
    print('fuck', file=sys.stderr)
    msg = ReturnMSG().no_selected_file
    return jsonify(msg)


@dishorderapi.route('/suppliers')
def hello_world2():
    msg = {}
    for i in range(1, 3):
        if i == 1:
            msg[i] = "TML Restaurant"
        if i == 2:
            msg[i] = "HKT Restaurant"
    return jsonify(msg)


@dishorderapi.route('/products', methods=['GET'])
def products():
    print(request.args.get('from'))
    # first_day_of_month_count_from_monday_of_previous_month
    date = calendar.monthrange(2019, 6)[0]
    # month have ? day
    month_have = calendar.monthrange(2019, 6)[1]
    previous_month_have = calendar.monthrange(2019, 5)[1]
    msg = {'previous_month': {}, 'this_month': {}}
    for i in range(previous_month_have - date + 1, previous_month_have + 1):
        msg['previous_month'][i] = i
    for i in range(1, month_have + 1):
        msg['this_month'][i] = i
    print(msg)
    return jsonify(msg)


@dishorderapi.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email_address = request.json.get('email_address')
        password = request.json.get('password')
        if not email_address or not password:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            users_object = session.query(Users).filter_by(email_address=email_address)
            if users_object.count() == 1:
                users_object = users_object[0]  # GET First Record
                if users_object.password == password:
                    msg = ReturnMSG().return_token
                    msg['msg'] = generate_auth_token(user_id=users_object.id,
                                                     profile=users_object.profile)
                    return jsonify(msg)
                else:
                    return jsonify(ReturnMSG().username_or_password_incorrect)
            elif users_object.count() == 0:
                return jsonify(ReturnMSG().username_or_password_incorrect)
            else:
                abort(500)
    else:
        jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/register', methods=['POST'])
def register():
    if request.is_json:
        email_address = request.json.get('email_address')
        password = request.json.get('password')
        first_name = request.json.get('first_name')
        family_name = request.json.get('family_name', None)
        photo_thumbnail = b''
        photo_default_id = 1
        creation_date = datetime.now(tz).timestamp()
        last_connection_date = 0
        profile = 0
        if not email_address or not password or not first_name:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            new_user = Users(email_address=email_address, password=password, first_name=first_name,
                             family_name=family_name,
                             photo_thumbnail=photo_thumbnail, photo_default_id=photo_default_id,
                             creation_date=creation_date,
                             last_connection_date=last_connection_date, profile=profile)
            session.add(new_user)
            session.commit()
            return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/dishes', methods=['GET'])
def dishes():
    query_string = request.args.get('querystring')
    msg = ReturnMSG().return_transaction_list
    if query_string:
        all_dishes = get_all_dishes(query_string=query_string)
    else:
        all_dishes = get_all_dishes()
    for record in all_dishes:
        print(record)
        dish_id, supplier_code, dish_type_code, dish_code, dish_description, unit_price, \
        currency, review, popularity, created_date, created_by, photo_thumbnail, photo_default_id \
            = [value for value in record]
        msg['msg'][dish_id] = {'supplier_code': supplier_code, 'dish_code': dish_code, 'popularity': popularity,
                               'photo_default_id': photo_default_id, 'unit_price': unit_price}
    return jsonify(msg)


@dishorderapi.route('/createdishes', methods=['POST'])
@login_required
def create_dish(guard_msg):
    if request.is_json:
        print('ok')
    else:
        print('not ok')


@dishorderapi.route('/create-supplier', methods=['GET'])
def create_supplier():
    if request.is_json:
        code = request.json.get('code')
        name = request.json.get('name')
        email_address = request.json.get('email_address')
        phone = request.json.get('phone')
        contact_name = request.json.get('contact_name')
        photo_thumbnail = b''
        photo_default_id = 2
        order_time_deadline = datetime.now(tz).timestamp()
        last_connection_date = 0
        profile = 0
        if not email_address or not password or not first_name:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            new_user = Users(email_address=email_address, password=password, first_name=first_name,
                             family_name=family_name,
                             photo_thumbnail=photo_thumbnail, photo_default_id=photo_default_id,
                             creation_date=creation_date,
                             last_connection_date=last_connection_date, profile=profile)
            session.add(new_user)
            session.commit()
            return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)
