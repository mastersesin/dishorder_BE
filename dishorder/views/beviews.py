import flask
from flask import jsonify, Blueprint, abort, Flask, send_file
from .functions import *
from .return_msg import ReturnMSG
from dishorder import session
from .models import *
import calendar
from werkzeug.utils import secure_filename
from sqlalchemy.exc import IntegrityError
import sys
import os
from sqlalchemy import update
import time
from dishorder.micro_service.automate_create_order import *
from dishorder.views.classes import FormValidator

dishorderapi = Blueprint('dishorderapi', __name__)


@dishorderapi.route('/img/<img_name>', methods=['GET'])
def img_serve(img_name):
    temp = app.config['UPLOAD_FOLDER'] + '/' + img_name
    return send_file(temp, mimetype='image/png')


@dishorderapi.route('/upload', methods=['POST'])
def upload():
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
        msg['msg'] = filename
        return jsonify(msg)


@dishorderapi.route('/test', methods=['GET'])
def test():
    # all_dishes = session.query(Dishes, Suppliers, Photos).join(Suppliers, Dishes.supplier_code == Suppliers.code).join(
    #     Photos, Dishes.photo_default_id == Photos.id).all()
    # for record in all_dishes:
    #     print(record[0].supplier_code, record[1].name, record[2].path)
    user_input_dish_tag = 'Beefcc'
    # record = session.query(DishTags).filter(DishTags.tags_name == user_input_dish_tag).all()
    new_tag = DishTags(tags_name=user_input_dish_tag)
    try:
        session.add(new_tag)
        session.commit()
    except IntegrityError as ex:
        print(ex.statement)
        import re
        print(re.findall("DETAIL:.+(\(.+\))", str(ex)))
        session.rollback()
    return 'hih'


@dishorderapi.route('/suppliers')
def suppliers():
    msg = ReturnMSG().return_supplier_list
    all_suppliers = session.query(Suppliers).all()
    for supplier in all_suppliers:
        photo_object = session.query(Photos).filter(Photos.id == supplier.photo_default_id).first()
        msg['msg'][str(supplier.code)] = supplier.serializable
        msg['msg'][str(supplier.code)]['image_URL'] = app.config['API_ADDRESS'] + \
                                                      app.config['IMG_URI'] + \
                                                      photo_object.path
    return jsonify(msg)
    # msg = {}
    # for i in range(1, 3):
    #     if i == 1:
    #         msg[i] = "TML Restaurant"
    #     if i == 2:
    #         msg[i] = "HKT Restaurant"
    # return jsonify(msg)


@dishorderapi.route('/products', methods=['GET'])
def products():
    print(request.args.get('from'))
    # first_day_of_month_count_from_monday_of_previous_month
    date = calendar.monthrange(2019, 7)[0]
    # month have ? day
    month_have = calendar.monthrange(2019, 7)[1]
    previous_month_have = calendar.monthrange(2019, 6)[1]
    msg = {'previous_month': {}, 'this_month': {}, 'which_month_is_this': 7}
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
        email_address = request.json.get('email_address', None)
        password = request.json.get('password', None)
        retype_password = request.json.get('retype_password', None)
        first_name = request.json.get('first_name', None)
        family_name = request.json.get('family_name', None)
        photo_thumbnail = b''
        photo_default_id = 1
        creation_date = get_timestamp_now()
        last_connection_date = 0
        profile = 0
        print(email_address, password, retype_password, first_name, family_name, file=sys.stderr)
        if not email_address or not password or not first_name or not retype_password:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            validator = FormValidator()
            if validator.email_validation(email_address):
                if validator.password_match(password, retype_password):
                    is_email_address_existed = session.query(Users).filter(Users.email_address == email_address).first()
                    if not is_email_address_existed:
                        new_user = Users(email_address=email_address, password=password, first_name=first_name,
                                         family_name=family_name,
                                         photo_thumbnail=photo_thumbnail, photo_default_id=photo_default_id,
                                         creation_date=creation_date,
                                         last_connection_date=last_connection_date, profile=profile)
                        session.add(new_user)
                        session.commit()
                        return jsonify(ReturnMSG().register_success)
                    else:
                        msg = ReturnMSG().fail_cheat
                        msg['msg'] = 'Email address {} existed'.format(email_address)
                        return jsonify(msg)
                else:
                    msg = ReturnMSG().fail_cheat
                    msg['msg'] = 'Password do not match'
                    return jsonify(msg)
            else:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Email address contain invalid character or incorrect format'
                return jsonify(msg)
    else:
        return jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/get-dish', methods=['GET'])
def dishes():
    dish_name_sort = request.args.get('dish_name', '%')
    suppliers_sort = request.args.get('supplier', '%')
    tag_sort = request.args.get('tag_sort', '%')
    msg = ReturnMSG().return_transaction_list
    if suppliers_sort or tag_sort or dish_name_sort:
        all_dishes = session.query(Dishes, Suppliers, Photos, DishTags) \
            .join(Suppliers, Dishes.supplier_code == Suppliers.code) \
            .join(Photos, Dishes.photo_default_id == Photos.id) \
            .join(DishTags, Dishes.dish_tag_id == DishTags.id) \
            .filter(Dishes.dish_name.like('%' + dish_name_sort + '%')) \
            .filter(Suppliers.code.like(suppliers_sort)) \
            .filter(DishTags.tags_name.like(tag_sort)).all()
    else:
        all_dishes = session.query(Dishes, Suppliers, Photos, DishTags) \
            .join(Suppliers, Dishes.supplier_code == Suppliers.code) \
            .join(Photos, Dishes.photo_default_id == Photos.id) \
            .join(DishTags, Dishes.dish_tag_id == DishTags.id).all()
    for dish in all_dishes:
        msg['msg'][dish[0].dish_id] = dish[0].serializable
        msg['msg'][dish[0].dish_id]['supplier_name'] = dish[1].name
        msg['msg'][dish[0].dish_id]['tags_name'] = dish[3].tags_name
        msg['msg'][dish[0].dish_id]['image_URL'] = app.config['API_ADDRESS'] + \
                                                   app.config['IMG_URI'] + \
                                                   dish[2].path
    return jsonify(msg)


@dishorderapi.route('/edit-dish', methods=['PUT'])
def edit_dish():
    if request.is_json:
        dish_id = request.json.get('dish_id')
        supplier = request.json.get('supplier')
        dish_name = request.json.get('dish_name')
        current_dish_name = session.query(Dishes).filter(Dishes.dish_id == dish_id).first()
        if current_dish_name.dish_name != dish_name:
            check_dish_name = session.query(Dishes).filter_by(dish_name=dish_name).first()
            if check_dish_name:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Dish name {} existed'.format(check_dish_name.dish_name)
                return jsonify(msg)
        dish_tag = request.json.get('dish_tag')
        dish_tag_id_query_from_input_dish_tag = session.query(DishTags).filter(
            DishTags.tags_name == dish_tag.title()).first()
        if dish_tag_id_query_from_input_dish_tag:
            dish_tag_id = dish_tag_id_query_from_input_dish_tag.id
        else:
            new_dish_tag = DishTags(tags_name=dish_tag.title())
            session.add(new_dish_tag)
            session.commit()
            dish_tag_id = new_dish_tag.id
        dish_description = request.json.get('dish_description')
        unit_price = request.json.get('unit_price', -1)
        unit_price = int(unit_price)
        currency = request.json.get('currency')
        uploaded_img_name = request.json.get('uploaded_img_name')
        need_to_update_this_dish = session.query(Dishes).filter(Dishes.dish_id == dish_id).first()
        if uploaded_img_name:
            new_supplier_photo = Photos(photo_type='supplier',
                                        type_id=0,
                                        path=uploaded_img_name)
            session.add(new_supplier_photo)
            session.commit()
            uploaded_img_id = session.query(Photos).filter_by(path=uploaded_img_name).first().id
            photo_default_id = uploaded_img_id
        else:
            photo_default_id = need_to_update_this_dish.photo_default_id
        new_dish = Dishes(supplier_code=supplier, dish_name=dish_name, dish_tag_id=dish_tag_id,
                          dish_description=dish_description, unit_price=unit_price, currency=currency,
                          review=0, popularity=0, created_date=0, created_by=0,
                          photo_thumbnail=b'', photo_default_id=photo_default_id)
        validation_return = new_dish.validation
        if not validation_return == "True":
            msg = ReturnMSG().fail_cheat
            msg['msg'] = validation_return
            return jsonify(msg)
        else:
            need_to_update_this_dish.supplier_code = supplier
            need_to_update_this_dish.dish_name = dish_name
            need_to_update_this_dish.dish_tag_id = dish_tag_id
            need_to_update_this_dish.dish_description = dish_description
            need_to_update_this_dish.unit_price = unit_price
            need_to_update_this_dish.currency = currency
            need_to_update_this_dish.photo_default_id = photo_default_id
            session.commit()
            return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/create-dish', methods=['POST'])
def create_dish():
    if request.is_json:
        supplier_code = request.json.get('supplier', '')
        dish_name = request.json.get('dish_name', '')
        is_dish_name_existed = session.query(Dishes).filter(Dishes.dish_name == dish_name).first()
        if is_dish_name_existed:
            msg = ReturnMSG().fail_cheat
            msg['msg'] = 'Supplier code {} existed'.format(dish_name)
            return jsonify(msg)
        dish_tag = request.json.get('dish_tag', '')
        if not dish_tag:
            msg = ReturnMSG().fail_cheat
            msg['msg'] = 'Dish tag contain invalid character or missing'
            return jsonify(msg)
        dish_tag_id_query_from_input_dish_tag = session.query(DishTags).filter(
            DishTags.tags_name == dish_tag.title()).first()
        if dish_tag_id_query_from_input_dish_tag:
            dish_tag_id = dish_tag_id_query_from_input_dish_tag.id
        else:
            new_dish_tag = DishTags(tags_name=dish_tag.title())
            session.add(new_dish_tag)
            session.commit()
            dish_tag_id = new_dish_tag.id
        dish_description = request.json.get('dish_description')
        unit_price = request.json.get('unit_price', -1)
        unit_price = int(unit_price)
        currency = request.json.get('currency', '')
        review = 0
        popularity = 0
        created_date = get_timestamp_now()
        created_by = 0
        photo_thumbnail = b''
        uploaded_img_name = request.json.get('uploaded_img_name')
        if uploaded_img_name:
            new_supplier_photo = Photos(photo_type='supplier',
                                        type_id=0,
                                        path=uploaded_img_name)
            session.add(new_supplier_photo)
            session.commit()
            uploaded_img_id = session.query(Photos).filter_by(path=uploaded_img_name).first().id
            photo_default_id = uploaded_img_id
        else:
            photo_default_id = 1
        new_dish = Dishes(supplier_code=supplier_code, dish_name=dish_name, dish_tag_id=dish_tag_id,
                          dish_description=dish_description, unit_price=unit_price, currency=currency,
                          review=review, popularity=popularity, created_date=created_date, created_by=created_by,
                          photo_thumbnail=photo_thumbnail, photo_default_id=photo_default_id)
        validation_return = new_dish.validation
        if not validation_return == "True":
            msg = ReturnMSG().fail_cheat
            msg['msg'] = validation_return
            return jsonify(msg)
        else:
            session.add(new_dish)
            session.commit()
            return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/create-supplier', methods=['POST'])
def create_supplier():
    if request.is_json:
        # Supplier code get json and validate if it existed
        code = request.json.get('code', '')
        is_code_existed = session.query(Suppliers).filter(Suppliers.code == code).first()
        if is_code_existed:
            msg = ReturnMSG().fail_cheat
            msg['msg'] = 'Supplier code {} existed'.format(code)
            return jsonify(msg)
        name = request.json.get('name', '')
        email_address = request.json.get('email_address', '')
        is_email_existed = session.query(Suppliers).filter(Suppliers.email_address == email_address).first()
        if is_email_existed:
            msg = ReturnMSG().fail_cheat
            msg['msg'] = 'Supplier email {} existed'.format(email_address)
            return jsonify(msg)
        phone = request.json.get('phone', '')
        contact_name = request.json.get('contact_name', '')
        currency = request.json.get('currency')
        photo_thumbnail = b''
        uploaded_img_name = request.json.get('uploaded_img_name')
        if uploaded_img_name:
            new_supplier_photo = Photos(photo_type='supplier',
                                        type_id=0,
                                        path=uploaded_img_name)
            session.add(new_supplier_photo)
            session.commit()
            uploaded_img_id = session.query(Photos).filter_by(path=uploaded_img_name).first().id
            photo_default_id = uploaded_img_id
        else:
            photo_default_id = 1
        order_time_deadline = hour_minute_to_timestamp(request.json.get('order_time_deadline', 0))
        minimum_order_quantity = int(request.json.get('min_quantity', '-1'))
        minimum_order_amount = int(request.json.get('min_amount', '-1'))
        review = 0
        popularity = 0
        if False:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            new_supplier = Suppliers(code=code, name=name, email_address=email_address, phone=phone,
                                     contact_name=contact_name, photo_thumbnail=photo_thumbnail, currency=currency,
                                     photo_default_id=photo_default_id, order_time_deadline=order_time_deadline,
                                     minimum_order_quantity=minimum_order_quantity,
                                     minimum_order_amount=minimum_order_amount,
                                     review=review, popularity=popularity)
            validation_return = new_supplier.validation
            if not validation_return == "True":
                msg = ReturnMSG().fail_cheat
                msg['msg'] = validation_return
                return jsonify(msg)
            else:
                # session.add(new_supplier)
                # session.commit()
                print(new_supplier)
                return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/edit-supplier', methods=['PUT'])
def edit_supplier():
    if request.is_json:
        current_code = request.json.get('current_code')
        code_change_to = request.json.get('code_change_to', '')
        is_code_existed = session.query(Suppliers).filter(Suppliers.code == code_change_to).first()
        if current_code != code_change_to:
            if is_code_existed:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Supplier code {} existed'.format(code_change_to)
                return jsonify(msg)
            else:
                pass
        else:
            pass
        name = request.json.get('name', '')
        email_address = request.json.get('email_address', '')
        supplier_current_email = session.query(Suppliers).filter_by(email_address=email_address).first()
        if supplier_current_email.email_address != email_address:
            check_email = session.query(Suppliers).filter_by(email_address=email_address).first()
            if check_email:
                msg = ReturnMSG().fail_cheat
                msg['msg'] = 'Supplier email {} existed'.format(email_address)
                return jsonify(msg)
        phone = request.json.get('phone', '')
        contact_name = request.json.get('contact_name', '')
        currency = request.json.get('currency', '')
        uploaded_img_name = request.json.get('uploaded_img_name')
        supplier_need_to_edit = session.query(Suppliers).filter_by(code=current_code).first()
        if uploaded_img_name:
            new_supplier_photo = Photos(photo_type='supplier',
                                        type_id=0,
                                        path=uploaded_img_name)
            session.add(new_supplier_photo)
            session.commit()
            uploaded_img_id = session.query(Photos).filter_by(path=uploaded_img_name).first().id
            photo_default_id = uploaded_img_id
        else:
            photo_default_id = supplier_need_to_edit.photo_default_id
        order_time_deadline = hour_minute_to_timestamp(request.json.get('order_time_deadline', 0))
        minimum_order_quantity = int(request.json.get('min_quantity', '-1'))
        minimum_order_amount = int(request.json.get('min_amount', '-1'))
        if False:
            return jsonify(ReturnMSG().wrong_post_format)
        else:
            new_supplier_check_obj = Suppliers(code=code_change_to, name=name, email_address=email_address, phone=phone,
                                               contact_name=contact_name, photo_thumbnail=b'', currency=currency,
                                               photo_default_id=photo_default_id,
                                               order_time_deadline=order_time_deadline,
                                               minimum_order_quantity=minimum_order_quantity,
                                               minimum_order_amount=minimum_order_amount,
                                               review=0, popularity=0)
            validation_return = new_supplier_check_obj.validation
            if not validation_return == "True":
                msg = ReturnMSG().fail_cheat
                msg['msg'] = validation_return
                return jsonify(msg)
            else:
                supplier_need_to_edit.code = code_change_to
                supplier_need_to_edit.name = name
                supplier_need_to_edit.email_address = email_address
                supplier_need_to_edit.phone = phone
                supplier_need_to_edit.contact_name = contact_name
                supplier_need_to_edit.currency = currency
                supplier_need_to_edit.order_time_deadline = order_time_deadline
                supplier_need_to_edit.minimum_order_quantity = int(minimum_order_quantity)
                supplier_need_to_edit.minimum_order_amount = int(minimum_order_amount)
                if photo_default_id:
                    supplier_need_to_edit.photo_default_id = photo_default_id
                else:
                    pass
                session.commit()
                return jsonify(ReturnMSG().register_success)
    else:
        return jsonify(ReturnMSG().wrong_post_format)


@dishorderapi.route('/get-tag', methods=['GET'])
def get_tag():
    all_tag = session.query(DishTags).all()
    msg = ReturnMSG().return_transaction_list
    for tag in all_tag:
        msg['msg'][tag.id] = tag.tags_name
    return jsonify(msg)


@dishorderapi.route('/get-dish-lay', methods=['GET'])
def dishes_lay():
    suppliers_sort = request.args.get('supplier', '')
    suppliers_sort = [x for x in suppliers_sort.split(',') if x != '']
    print(suppliers_sort)
    tag_sort = request.args.get('tag_sort', '')
    tag_sort = [x for x in tag_sort.split(',') if x != '']
    msg = ReturnMSG().return_transaction_list
    # if suppliers_sort or tag_sort:
    all_dishes = session.query(Dishes, Suppliers, Photos, DishTags) \
        .join(Suppliers, Dishes.supplier_code == Suppliers.code) \
        .join(Photos, Dishes.photo_default_id == Photos.id) \
        .join(DishTags, Dishes.dish_tag_id == DishTags.id)
    if len(suppliers_sort) > 0 and len(tag_sort) == 0:
        print('1')
        record = all_dishes.filter(Suppliers.code.in_(suppliers_sort)).all()
    elif len(tag_sort) > 0 and len(suppliers_sort) == 0:
        print('2')
        record = all_dishes.filter(DishTags.tags_name.in_(tag_sort)).all()
    elif len(tag_sort) > 0 and len(suppliers_sort) > 0:
        print('3')
        record = all_dishes.filter(Suppliers.code.in_(suppliers_sort)) \
            .filter(DishTags.tags_name.in_(tag_sort)).all()
    else:
        record = all_dishes.all()
    for dish in record:
        msg['msg'][dish[0].dish_id] = dish[0].serializable
        msg['msg'][dish[0].dish_id]['supplier_name'] = dish[1].name
        msg['msg'][dish[0].dish_id]['tags_name'] = dish[3].tags_name
        msg['msg'][dish[0].dish_id]['image_URL'] = app.config['API_ADDRESS'] + \
                                                   app.config['IMG_URI'] + \
                                                   dish[2].path
    return jsonify(msg)


@dishorderapi.route('/foodorder', methods=['POST'])
def food_order():
    dishchoose = request.json.get('dishchoose')
    is_checked_order = []
    for dish in dishchoose:
        order_day = dishchoose[dish]['orderday']
        order_month = dishchoose[dish]['ordermonth']
        if dishchoose[dish]['value']['supplier_code'] not in is_checked_order:
            order_id = session.query(OrdersToSuppliers) \
                .filter(OrdersToSuppliers.order_date == get_timestamp_by(order_month, order_day)) \
                .filter(OrdersToSuppliers.supplier_code == dishchoose[dish]['value']['supplier_code']) \
                .first()
            if order_id:
                order_id = order_id.order_id
            else:
                new_order_to_supplier = OrdersToSuppliers(supplier_code=dishchoose[dish]['value']['supplier_code'],
                                                          order_date=get_timestamp_by(order_month,
                                                                                      order_day),
                                                          delivery_address='DI',
                                                          total_amount=0,
                                                          currency='VND',
                                                          created_date=get_timestamp_now(),
                                                          created_by=0,
                                                          sent_date=None,
                                                          order_comment='')
                session.add(new_order_to_supplier)
                session.commit()
                order_id = new_order_to_supplier.order_id
            is_checked_order.append(dishchoose[dish]['value']['supplier_code'])
        else:
            pass
        print(dishchoose[dish]['value'])
        token = request.json.get('token')
        print(decode_auth_token(token=token))
        order_id = order_id
        order_date = get_timestamp_by(order_month, order_day)
        user_id = decode_auth_token(token=token)['id']
        on_behalf_of_customer = dishchoose[dish]['onbehalf']
        dish_id = dishchoose[dish]['key']
        quantity = dishchoose[dish]['quantity']
        unit_price = dishchoose[dish]['value']['unit_price']
        currency = dishchoose[dish]['value']['currency']
        created_date = get_timestamp_now()
        created_by = order_id
        review = 0
        review_comment = None
        new_order = CustomerOrders(order_id=order_id,
                                   order_date=order_date, user_id=user_id,
                                   on_behalf_of_customer=on_behalf_of_customer, dish_id=dish_id,
                                   quantity=quantity, unit_price=unit_price, currency=currency,
                                   created_date=created_date, created_by=created_by, review=review,
                                   review_comment=review_comment)
        session.add(new_order)
        session.commit()
        update_order_to_supplier(order_id)
    return jsonify(ReturnMSG().register_success)


@dishorderapi.route('/getallorders', methods=['GET'])
def get_all_order():
    all_order = session.query(OrdersToSuppliers).all()
    msg = ReturnMSG().return_transaction_list
    for order in all_order:
        msg['msg'][order.order_id] = order.serializable
    return jsonify(msg)


@dishorderapi.route('/getalluserorders', methods=['GET'])
def get_all_user_order():
    supplier = request.args.get('supplier')
    order_day = request.args.get('order_day')
    all_order = session.query(CustomerOrders, Users, Dishes) \
        .join(Users, CustomerOrders.user_id == Users.id) \
        .join(Dishes, CustomerOrders.dish_id == Dishes.dish_id) \
        .filter(Dishes.supplier_code == supplier) \
        .filter(CustomerOrders.order_date >= get_timestamp_by(7, order_day)) \
        .filter(CustomerOrders.order_date < get_timestamp_by(7, order_day) + 86400) \
        .all()
    print(all_order)
    msg = ReturnMSG().return_transaction_list
    for order in all_order:
        print(order)
        msg['msg'][order[0].customer_order_id] = order[0].serializable
        msg['msg'][order[0].customer_order_id]['user_name'] = order[1].first_name
        msg['msg'][order[0].customer_order_id]['dish_name'] = order[2].dish_name
    print(msg)
    return jsonify(msg)
