from flask import request, jsonify, Blueprint, abort
from .functions import *
from .return_msg import ReturnMSG
from .sql_query import *
from dishorder import app, db
from dishorder.views.models import Users, Photos
import calendar

dishorderapi = Blueprint('dishorderapi', __name__)


@dishorderapi.route('/products')
def products():
    db.session.add(Users(email_address="example@example.com", password="hihi", first_name="ty", photo_default_id=0,
                         creation_date="2015-09-01T16:34:02", last_connection_date="2015-09-01T16:34:02", profile=0,
                         family_name="", photo_thumbnail=b""))
    db.session.commit()
    return "hihi"


@dishorderapi.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json.get('email')
        password = request.json.get('password')
        print(email)
        print(password)
        if not email or not password:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            users_object = Users.query.filter_by(email_address='example@example.com')
            print(users_object.first().password)
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
        email = request.json.get('email')
        password = request.json.get('password')
        first_name = request.json.get('first_name')
        if not email or not password or not first_name:
            return jsonify(ReturnMSG().wrong_post_format)
        # --------------------
        # Validation step
        # --------------------
        # PASS it for now because we don`t have much time
        else:
            add_user(email_address=email, password=password, first_name=first_name)
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


@dishorderapi.route('/createsupplier', methods=['POST'])
@login_required
def create_dish1(guard_msg):
    if request.is_json:
        print('ok')
    else:
        print('not ok')
