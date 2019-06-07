from dishorder import db


class Photos(db.Model):
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
    id = db.Column(db.Integer, primary_key=True)
    email_address = db.Column(db.String, unique=True, nullable=False)
    password = db.Column(db.String, nullable=False)
    first_name = db.Column(db.String, nullable=False)
    family_name = db.Column(db.String)
    photo_thumbnail = db.Column(db.LargeBinary)
    photo_default_id = db.Column(db.Integer, default=0, nullable=False)
    creation_date = db.Column(db.DateTime, default=0, nullable=False)
    last_connection_date = db.Column(db.DateTime, default=0, nullable=False)
    profile = db.Column(db.Integer, default=0)

    def __init__(self, email_address, password, first_name, family_name, photo_thumbnail, photo_default_id,
                 creation_date
                 , last_connection_date, profile):
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
