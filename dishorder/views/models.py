from sqlalchemy import Column, Integer, String, LargeBinary, ForeignKey, REAL
from sqlalchemy.orm import relationship
from dishorder import Base
from .functions import *
import re
import calendar


class Photos(Base):
    __tablename__ = 'photo'
    id = Column(Integer, primary_key=True)
    photo_type = Column(String, nullable=False)
    type_id = Column(Integer)
    path = Column(String, unique=True, nullable=False)

    def __init__(self, photo_type, type_id, path):
        self.photo_type = photo_type
        self.type_id = type_id
        self.path = path

    def __repr__(self):
        return '<Photos %d>' % self.id


class Users(Base):
    __tablename__ = 'user'
    id = Column(Integer, primary_key=True)
    email_address = Column(String, unique=True, nullable=False)
    password = Column(String, nullable=False)
    first_name = Column(String, nullable=False)
    family_name = Column(String)
    photo_thumbnail = Column(LargeBinary)
    photo_default_id = Column(Integer, ForeignKey('photo.id'), default=0, nullable=False)
    photo_default_id_relationship = relationship('Photos', backref='user')
    creation_date = Column(Integer, default=0, nullable=False)
    last_connection_date = Column(Integer, default=0, nullable=False)
    profile = Column(Integer, default=0)
    register_proposal_status = Column(Integer, default=0)
    register_secret_code = Column(Integer, default=0)

    def __repr__(self):
        return '<User %d>' % self.id

    @property
    def validation(self):
        password = re.compile('^[a-zA-Z0-9 ].+')
        email_address = re.compile('[^@]+@[^@]+\.[^@]+')
        first_name = re.compile('^[a-zA-Z ]+[a-zA-Z ]$')
        if not email_address.match(self.email_address):
            return "Email address contain invalid character or missing"
        if not password.match(self.password):
            return "Password contain invalid character or missing"
        if not first_name.match(self.first_name):
            return "First name contain invalid character or missing"
        return "True"


class Suppliers(Base):
    __tablename__ = 'supplier'
    code = Column(String, nullable=False, primary_key=True)
    name = Column(String, nullable=False)
    email_address = Column(String, unique=True, nullable=False)
    phone = Column(String)
    contact_name = Column(String)
    photo_thumbnail = Column(LargeBinary)
    photo_default_id = Column(Integer, ForeignKey('photo.id'), default=0, nullable=False)
    supplier_photo_default_id_relationship = relationship('Photos', backref='supplier')
    order_time_deadline = Column(Integer, nullable=False)
    minimum_order_quantity = Column(Integer, default=1)
    minimum_order_amount = Column(REAL, default=0)
    currency = Column(String, default='VND', nullable=False)
    review = Column(Integer, default=0, nullable=False)
    popularity = Column(Integer, default=0, nullable=False)

    def __repr__(self):
        return '<Supplier %s>' % self.code

    @property
    def validation(self):
        code = re.compile('^[a-zA-Z0-9]+[a-zA-Z0-9]$')
        name = re.compile('^[a-zA-Z0-9 ]+[a-zA-Z0-9 ]$')
        phone = re.compile('^0\d{8,10}$')
        email_address = re.compile('[^@]+@[^@]+\.[^@]+')
        if not code.match(self.code):
            return "Supplier code contain invalid character or missing"
        if not name.match(self.name):
            return "Supplier name contain invalid character or missing"
        if not email_address.match(self.email_address):
            return "Supplier email address contain invalid character or missing"
        if not phone.match(self.phone):
            return "Supplier phone contain invalid character or missing"
        # if not name.match(self.contact_name):
        #     return "Supplier contact name"
        if self.minimum_order_quantity > 999999 or self.minimum_order_quantity < 0:
            return "Minimum order quantity not in range 0-999999"
        if self.minimum_order_amount > 999999 or self.minimum_order_amount < 0:
            return "Minimum order amount not in range 0-999999"
        if self.order_time_deadline == 0:
            return "Order time deadline contain invalid character or missing"
        return "True"

    @property
    def serializable(self):
        return {
            'code': self.code,
            'name': self.name,
            'email_address': self.email_address,
            'phone': self.phone,
            'contact_name': self.contact_name,
            'photo_thumbnail': '',  # self.photo_thumbnail,
            'photo_default_id': self.photo_default_id,
            'order_time_deadline': timestamp_to_hour_minute(self.order_time_deadline),
            'minimum_order_quantity': self.minimum_order_quantity,
            'minimum_order_amount': self.minimum_order_amount,
            'currency': self.currency,
            'review': self.review,
            'popularity': self.popularity
        }


class Dishes(Base):
    __tablename__ = 'dish'
    dish_id = Column(Integer, nullable=False, primary_key=True)
    supplier_code = Column(String, ForeignKey('supplier.code'), nullable=False)
    supplier_code_relationship = relationship('Suppliers', backref='dishes')
    dish_name = Column(String, unique=True, nullable=False)
    dish_tag_id = Column(Integer, ForeignKey('dish_tag.id'), nullable=False)
    dish_tag_id_relationship = relationship('DishTags', backref='dish')
    dish_description = Column(String)
    unit_price = Column(String)
    currency = Column(String, default='VND', nullable=False)
    review = Column(Integer, default=0, nullable=False)
    popularity = Column(Integer, default=0, nullable=False)
    created_date = Column(Integer, default=0)
    created_by = Column(Integer, default=0, nullable=False)
    photo_thumbnail = Column(LargeBinary)
    photo_default_id = Column(Integer, ForeignKey('photo.id'), default=0, nullable=False)
    dishes_photo_default_id_relationship = relationship('Photos', backref='dishes')

    def __repr__(self):
        return '<Dish %d>' % self.dish_id

    @property
    def validation(self):
        print(self.unit_price)
        dish_name = re.compile('^[a-zA-Z0-9 ]+[a-zA-Z0-9 ]$')
        supplier_code = re.compile('^[A-Za-z].[A-Za-z]$')
        if not supplier_code.match(self.supplier_code):
            return "Supplier code not yet specified"
        if not dish_name.match(self.dish_name):
            return "Dish name contain invalid character or missing"
        if self.unit_price > 99999999 or self.unit_price < 0:
            return "Price amount not in range 0 - 99999999"
        return "True"

    @property
    def serializable(self):
        return {
            'dish_id': self.dish_id,
            'supplier_code': self.supplier_code,
            'dish_name': self.dish_name,
            'dish_tag_id': self.dish_tag_id,
            'dish_description': self.dish_description,
            'unit_price': self.unit_price,
            'photo_default_id': self.photo_default_id,
            'currency': self.currency,
            'review': self.review,
            'popularity': self.popularity,
            'created_date': self.created_date,
            'created_by': self.created_by,
            'photo_default_id': self.photo_default_id
        }


class DishTags(Base):
    __tablename__ = 'dish_tag'
    id = Column(Integer, primary_key=True, nullable=False, unique=True)
    tags_name = Column(String, nullable=False, unique=True, )

    # def __init__(self, dish_id, tags_name):
    #     self.dish_id = dish_id
    #     self.tags_name = tags_name

    def __repr__(self):
        return '<TAG %s>' % self.tags_name


class CustomerOrders(Base):
    __tablename__ = 'customer_order'
    customer_order_id = Column(Integer, nullable=False, primary_key=True)
    order_id = Column(Integer, ForeignKey('order_to_supplier.order_id'), default=0, nullable=False)
    order_id_relationship = relationship('OrdersToSuppliers', backref='customer_order')
    order_date = Column(Integer, nullable=False)
    user_id = Column(Integer, nullable=False)
    on_behalf_of_customer = Column(String, nullable=False)
    dish_id = Column(Integer, ForeignKey('dish.dish_id'), nullable=False)
    dish_id_relationship = relationship('Dishes', backref='customer_order')
    quantity = Column(Integer, default=1, nullable=False)
    unit_price = Column(REAL, nullable=False)
    currency = Column(String, default='VND', nullable=False)
    personal_comment = Column(String)
    created_date = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    review = Column(Integer, default=0, nullable=False)
    review_comment = Column(String)

    def __repr__(self):
        return '<CustomerOrdersNUM %d>' % self.customer_order_id

    @property
    def serializable(self):
        return {
            'on_behalf_of_customer': self.on_behalf_of_customer,
            'quantity': self.quantity,
            'unit_price': self.unit_price,
        }


class OrdersToSuppliers(Base):
    __tablename__ = 'order_to_supplier'
    order_id = Column(Integer, nullable=False, primary_key=True)
    supplier_code = Column(String, ForeignKey('supplier.code'), nullable=False)
    supplier_code_relationship = relationship('Suppliers', backref='order_to_supplier')
    order_date = Column(Integer, nullable=False)
    delivery_address = Column(String, nullable=False)
    total_amount = Column(REAL, nullable=False)
    currency = Column(String, default='VND', nullable=False)
    order_comment = Column(String)
    created_date = Column(Integer, nullable=False)
    created_by = Column(Integer, nullable=False)
    sent_date = Column(Integer)

    def __repr__(self):
        return '<OrdersToSupplierNUM %d>' % self.order_id

    @property
    def serializable(self):
        dtobj = datetime.fromtimestamp(self.order_date)
        return {
            'order_id': self.order_id,
            'supplier_code': self.supplier_code,
            'order_day': '{}'.format(dtobj.day),
            'order_month': '{}'.format(calendar.month_name[dtobj.month]),
            'order_day_word': '{}'.format(calendar.day_name[(1 % 7 - 1) + 3]),
            'delivery_address': self.delivery_address,
            'total_amount': self.total_amount,
            'currency': self.currency,
            'order_comment': self.order_comment,
            'created_date': self.created_date,
            'created_by': self.created_by,
            'sent_date': self.sent_date,
        }
