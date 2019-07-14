import re


class FormValidator:
    @staticmethod
    def email_validation(input_string):
        email_address = re.compile('[^@]+@[^@]+\.[^@]+')
        if not email_address.match(input_string):
            return False
        else:
            return True

    @staticmethod
    def password_match(password, retype_password):
        if password != retype_password:
            return False
        else:
            return True
