class ReturnMSG:
    def __init__(self):
        self.register_success = {"code": 1, "msg": "User created successfully."}
        self.username_or_password_incorrect = {"code": 5, "msg": "Username or Password Incorrect"}
        self.return_token = {"code": 6, "msg": ""}  # Dynamic msg so not show here
        self.wrong_post_format = {"code": 7, "msg": "Required form is missing or not in correct format"}
        self.wrong_method = {"code": 8, "msg": "Method not allow"}
        self.password_change_successfully = {"code": 9, "msg": "Password has changed successfully."}
        self.return_transaction_list = {"code": 10, "msg": {}}
        self.return_card_info = {"code": 11, "msg": {}}
        self.token_expired = {"code": 13, "msg": "Token Expired"}
        self.return_coupons_of_card = {"code": 12, "msg": {}}
        self.logout = {"code": 13, "msg": "Logout successfully."}

    def register_success(self):
        return self.register_success

    def username_or_password_incorrect(self):
        return self.username_or_password_incorrect

    def return_token(self):
        return self.return_token

    def four_hundred(self):
        return self.four_hundred

    def password_change_successfully(self):
        return self.password_change_successfully

    def return_transaction_list(self):
        return self.return_transaction_list

    def return_card_info(self):
        return self.return_card_info

    def token_expired(self):
        return self.token_expired

    def wrong_post_format(self):
        return self.wrong_post_format

    def logout(self):
        return self.logout
