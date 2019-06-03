from flask import request, jsonify, Blueprint, abort
from .functions import *
from .return_msg import ReturnMSG
from .sql_query import *
import datetime
import calendar

dishorderapi = Blueprint('dishorderapi', __name__)


@dishorderapi.route('/login', methods=['POST'])
def login():
    if request.is_json:
        email = request.json.get('email')
        password = request.json.get('password')
        print(email)
        if not email or not password:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            data_return_from_sql = [record for record in login_check(email_address=email, password=password)]
            if len(data_return_from_sql) == 1:
                print(data_return_from_sql[0])
                user_id, email_address, password, first_name, family_name, photo_thumbnail, photo_default_id, \
                creation_date, last_connection_date, profile = data_return_from_sql[0]
                msg = ReturnMSG().return_token
                msg['msg'] = generate_auth_token(user_id=user_id, profile=profile)
                return jsonify(msg)
            elif len(data_return_from_sql) == 0:
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


@app.route('/ldap')
def hello_world():
    print(request.args.get('from'))
    # first_day_of_month_count_from_monday_of_previous_month
    date = calendar.monthrange(2019, 5)[0]
    # month have ? day
    month_have = calendar.monthrange(2019, 5)[1]
    previous_month_have = calendar.monthrange(2019, 4)[1]
    msg = {'previous_month': {}, 'this_month': {}}
    for i in range(previous_month_have - date + 1, previous_month_have + 1):
        msg['previous_month'][i] = i
    for i in range(1, month_have + 1):
        msg['this_month'][i] = i
    print(msg)
    return jsonify(msg)


@app.route('/suppliers')
def hello_world2():
    msg = {}
    for i in range(1, 3):
        if i == 1:
            msg[i] = "TML Restaurant"
        if i == 2:
            msg[i] = "HKT Restaurant"
    return jsonify(msg)
