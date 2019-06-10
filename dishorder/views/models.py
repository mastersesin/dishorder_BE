from dishorder import db


class Photos(db.Model):
    __tablename__ = 'photo'
    id = db.Column(db.Integer, primary_key=True)
    photo_type = db.Column(db.String, nullable=False)
    type_id = db.Column(db.Integer)
    path = db.Column(db.String)

    def __init__(self, photo_type, type_id, path):
        self.photo_type = photo_type
        self.type_id = type_id
        self.path = path

    def __repr__(self):
        return '<Photos %d>' % self.id


class Users(db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    family_name = db.Column(db.String)
    photo_thumbnail = db.Column(db.LargeBinary)
    photo_default_id = db.Column(db.Integer, db.ForeignKey('photo.id'), default=0, nullable=False)
    photo_default_id_relationship = db.relationship("Photos", backref='user')
    creation_date = db.Column(db.Integer, default=0, nullable=False)
    last_connection_date = db.Column(db.Integer, default=0, nullable=False)
    profile = db.Column(db.Integer, default=0)

    def __init__(self, email_address, password, first_name, family_name, photo_thumbnail, photo_default_id,
                 creation_date, last_connection_date, profile):
        self.email_address = email_address
        self.password = password
        self.first_name = first_name
        self.family_name = family_name
        self.photo_thumbnail = photo_thumbnail
        self.photo_default_id = photo_default_id
        self.creation_date = creation_date
        self.last_connection_date = last_connection_date
        self.profile = profile

    def __repr__(self):
        return '<User %d>' % self.id


class Suppliers(db.Model):
    __tablename__ = 'supplier'
    code = db.Column(db.String, nullable=False, primary_key=True)
    name = db.Column(db.String, nullable=False)
    email_address = db.Column(db.String, unique=True, nullable=False)
    phone = db.Column(db.String)
    contact_name = db.Column(db.String)
    photo_thumbnail = db.Column(db.LargeBinary)
    photo_default_id = db.Column(db.Integer, db.ForeignKey('photo.id'), default=0, nullable=False)
    supplier_photo_default_id_relationship = db.relationship('Photos', backref='supplier')
    order_time_deadline = db.Column(db.Integer, nullable=False)
    minimum_order_quantity = db.Column(db.Integer, default=1)
    minimum_order_amount = db.Column(db.REAL, default=0)
    currency = db.Column(db.String, default='VND', nullable=False)
    review = db.Column(db.Integer, default=0, nullable=False)
    popularity = db.Column(db.Integer, default=0, nullable=False)

    def __init__(self, code, name, email_address, phone, contact_name,
                 photo_thumbnail,
                 photo_default_id, order_time_deadline, minimum_order_quantity,
                 minimum_order_amount,
                 currency, review, popularity):
        self.code = code
        self.name = name
        self.email_address = email_address
        self.phone = phone
        self.contact_name = contact_name
        self.photo_thumbnail = photo_thumbnail
        self.photo_default_id = photo_default_id
        self.order_time_deadline = order_time_deadline
        self.minimum_order_quantity = minimum_order_quantity
        self.minimum_order_amount = minimum_order_amount
        self.currency = currency
        self.review = review
        self.popularity = popularity

    def __repr__(self):
        return '<Supplier %d>' % self.code


class Dishes(db.Model):
    __tablename__ = 'dish'
    dish_id = db.Column(db.Integer, nullable=False, primary_key=True)
    supplier_code = db.Column(db.String, db.ForeignKey('supplier.code'), nullable=False)
    supplier_code_relationship = db.relationship('Suppliers', backref='dishes')
    dish_type_code = db.Column(db.String, unique=True, nullable=False)
    dish_code = db.Column(db.String, unique=True, nullable=False)
    dish_description = db.Column(db.String)
    unit_price = db.Column(db.String)
    currency = db.Column(db.String, default='VND', nullable=False)
    review = db.Column(db.Integer, default=0, nullable=False)
    popularity = db.Column(db.Integer, default=0, nullable=False)
    created_date = db.Column(db.Integer, default=0)
    created_by = db.Column(db.Integer, default=0, nullable=False)
    photo_thumbnail = db.Column(db.LargeBinary)
    photo_default_id = db.Column(db.Integer, db.ForeignKey('photo.id'), default=0, nullable=False)
    dishes_photo_default_id_relationship = db.relationship('Photos', backref='dishes')

    def __init__(self, dish_id, supplier_code, dish_type_code, dish_code, dish_description,
                 unit_price, created_by, review, popularity, created_date, currency):
        self.dish_id = dish_id
        self.supplier_code = supplier_code
        self.dish_type_code = dish_type_code
        self.dish_code = dish_code
        self.dish_description = dish_description
        self.unit_price = unit_price
        self.currency = currency
        self.review = review
        self.popularity = popularity
        self.created_date = created_date
        self.created_by = created_by
        self.review = review
        self.popularity = popularity

    def __repr__(self):
        return '<Supplier %d>' % self.code


class DishTags(db.Model):
    __tablename__ = 'dish_tag'
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), primary_key=True, nullable=False)
    dish_id_relationship = db.relationship('Dishes', backref='dish_tag')
    tags_name = db.Column(db.String, primary_key=True, nullable=False)

    def __init__(self, dish_id, tags_name):
        self.dish_id = dish_id
        self.tags_name = tags_name

    def __repr__(self):
        return '<TAG %d>' % self.tags_name


class CustomerOrders(db.Model):
    __tablename__ = 'customer_order'
    customer_order_id = db.Column(db.Integer, nullable=False, primary_key=True)
    order_id = db.Column(db.Integer, db.ForeignKey('user.id'), default=0, nullable=False)
    order_id_relationship = db.relationship('Users', backref='customer_order')
    order_date = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, nullable=False)
    on_behalf_of_customer = db.Column(db.String, nullable=False)
    dish_id = db.Column(db.Integer, db.ForeignKey('dish.dish_id'), nullable=False)
    dish_id_relationship = db.relationship('Dishes', backref='customer_order')
    quantity = db.Column(db.Integer, default=1, nullable=False)
    unit_price = db.Column(db.REAL, nullable=False)
    currency = db.Column(db.String, default='VND', nullable=False)
    personal_comment = db.Column(db.String)
    created_date = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    review = db.Column(db.Integer, default=0, nullable=False)
    review_comment = db.Column(db.String)

    def __init__(self, customer_order_id, order_id, order_date, user_id, on_behalf_of_customer, dish_id, quantity
                 , unit_price, currency, personal_comment, created_date, created_by, review, review_comment):
        self.customer_order_id = customer_order_id
        self.order_id = order_id
        self.order_date = order_date
        self.user_id = user_id
        self.on_behalf_of_customer = on_behalf_of_customer
        self.dish_id = dish_id
        self.quantity = quantity
        self.unit_price = unit_price
        self.currency = currency
        self.personal_comment = personal_comment
        self.created_date = created_date
        self.created_by = created_by
        self.review = review
        self.review_comment = review_comment

    def __repr__(self):
        return '<CustomerOrdersNUM %d>' % self.customer_order_id


class OrdersToSuppliers(db.Model):
    __tablename__ = 'order_to_supplier'
    order_id = db.Column(db.Integer, nullable=False, primary_key=True)
    supplier_code = db.Column(db.String, db.ForeignKey('supplier.code'), nullable=False)
    supplier_code_relationship = db.relationship('Suppliers', backref='order_to_supplier')
    order_date = db.Column(db.Integer, nullable=False)
    delivery_address = db.Column(db.String, nullable=False)
    total_amount = db.Column(db.REAL, nullable=False)
    currency = db.Column(db.String, default='VND', nullable=False)
    order_comment = db.Column(db.String)
    created_date = db.Column(db.Integer, nullable=False)
    created_by = db.Column(db.Integer, nullable=False)
    sent_date = db.Column(db.Integer, nullable=False)

    def __init__(self, order_id, supplier_code, order_date, delivery_address, total_amount, currency, order_comment
                 , created_date, created_by, sent_date):
        self.order_id = order_id
        self.supplier_code = supplier_code
        self.order_date = order_date
        self.delivery_address = delivery_address
        self.total_amount = total_amount
        self.currency = currency
        self.order_comment = order_comment
        self.created_date = created_date
        self.created_by = created_by
        self.sent_date = sent_date

    def __repr__(self):
        return '<OrdersToSupplierNUM %d>' % self.order_id
