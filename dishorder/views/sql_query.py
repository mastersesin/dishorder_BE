from sqlalchemy import create_engine

engine = create_engine('postgresql+pg8000://mastersesin:ckiuzk4ever@localhost:5432/dishorder')


def add_user(**kwargs):
    email_address = kwargs.get('email_address')
    password = kwargs.get('password')
    first_name = kwargs.get('first_name')
    family_name = kwargs.get('family_name', '')
    photo_thumbnail = kwargs.get('photo_thumbnail', '')
    photo_default_id = kwargs.get('photo_default_id', '1')
    creation_date = kwargs.get('creation_date', '0')
    last_connection_date = kwargs.get('last_connection_date', '0')
    engine.execute(
        """
            INSERT INTO users (
                email_address, password, first_name, family_name, photo_thumbnail,
                photo_default_id, creation_date, last_connection_date
            )
            VALUES ('{0}', '{1}', '{2}', nullif('{3}',''), '{4}', '{5}', '{6}', '{7}')
        """.format(
            email_address, password, first_name, family_name, photo_thumbnail,
            photo_default_id, creation_date, last_connection_date
        )
    )


def login_check(**kwargs):
    email_address = kwargs.get('email_address')
    password = kwargs.get('password')
    records_obj = engine.execute(
        """
            SELECT * FROM users
            WHERE email_address = '{0}' AND password = '{1}'
        """.format(
            email_address, password
        )
    )
    return records_obj.fetchall()


def add_supplier(**kwargs):
    supplier_code = kwargs.get('supplier_code')
    supplier_name = kwargs.get('supplier_name')
    email_address = kwargs.get('email_address')
    phone_number = kwargs.get('phone_number')
    contact_name = kwargs.get('contact_name')
    photo_thumbnail = kwargs.get('photo_thumbnail')
    photo_default_id = kwargs.get('photo_default_id', 1)
    order_time_deadline = kwargs.get('order_time_deadline', 0)
    minimum_order_quantity = kwargs.get('minimum_order_quantity', 0)
    minimum_order_amount = kwargs.get('minimum_order_amount', 0)
    currency = kwargs.get('currency', 'VND')
    review = kwargs.get('review', 0)
    popularity = kwargs.get('popularity', 0)
    engine.execute(
        """
            INSERT INTO suppliers( supplier_code, supplier_name, email_address, phone_number, contact_name,
            photo_thumbnail, photo_default_id, order_time_deadline, minimum_order_quantity, minimum_order_amount,
            currency, review, popularity)
            VALUES ('{0}', '{1}', '{2}', NULLIF('{3}','None'), NULLIF('{4}','None'), '{5}', '{6}', '{7}',
            '{8}', '{9}', '{10}', '{11}' ,'{12}')
        """.format(supplier_code, supplier_name, email_address, phone_number, contact_name, photo_thumbnail,
                   photo_default_id, order_time_deadline, minimum_order_quantity, minimum_order_amount,
                   currency, review, popularity)
    )


def add_dishes(**kwargs):
    supplier_code = kwargs.get('supplier_code')
    dish_type_code = kwargs.get('dish_type_code', 0)
    dish_code = kwargs.get('dish_code')
    dish_description = kwargs.get('dish_description')
    unit_price = kwargs.get('unit_price')
    currency = kwargs.get('currency', 'VND')
    review = kwargs.get('review', 0)
    popularity = kwargs.get('popularity', 0)
    created_date = kwargs.get('created_date', 0)
    created_by = kwargs.get('created_by', 0)
    photo_thumbnail = kwargs.get('photo_thumbnail')
    photo_default_id = kwargs.get('photo_default_id', '1')
    engine.execute(
        """
            INSERT INTO dishes (supplier_code, dish_type_code, dish_code, dish_description, unit_price,
            currency, review, popularity, created_date, created_by, photo_thumbnail, photo_default_id)
            VALUES ('{0}', '{1}', '{2}', NULLIF('{3}', 'None'), '{4}', '{5}', NULLIF('{6}', 0),
                    NULLIF('{7}', 0), '{8}', '{9}', '{10}', '{11}')
        """.format(supplier_code, dish_type_code, dish_code, dish_description, unit_price, currency, review, popularity,
                   created_date, created_by, photo_thumbnail, photo_default_id)
    )


def get_all_dishes(**kwargs):
    query_string = kwargs.get('query_string')
    if not query_string:
        print('1')
        print(query_string)
        records = engine.execute(
            """
                SELECT * FROM dishes
            """
        )
    else:
        print(query_string)
        records = engine.execute(
            """
                SELECT * FROM dishes
                WHERE dishes.dish_code LIKE '{}%'
            """.format(query_string)
        )
    re_records = records.fetchall()
    records.close()
    return re_records
