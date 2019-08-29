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
        self.no_file_part = {"code": 14, "msg": "No file part."}
        self.no_selected_file = {"code": 15, "msg": "No selected file."}
        self.upload_successfully = {"code": 16, "msg": "Upload successfully."}
        self.return_supplier_list = {"code": 17, "msg": {}}
        self.supplier_code_existed = {"code": 18, "msg": "Supplier code existed"}
        self.supplier_name_existed = {"code": 19, "msg": "Supplier name existed"}
        self.supplier_email_existed = {"code": 19, "msg": "Supplier email existed"}
        self.supplier_code_invalid = {"code": 20, "msg": "Supplier code contain invalid character"}
        self.fail_cheat = {"code": 21, "msg": ""}
        self.permission_denied = {"code": 22, "msg": "Permission Denied"}
        self.four_hundred = {"code": 23, "msg": "No No No"}
        self.delete_order_success = {"code": 24, "msg": "Delete OK"}
        self.order_not_exist = {"code": 25, "msg": "Order not exist"}
        self.login_proposal_not_yet_accepted = {"code": 26, "msg": "Login proposal not yet accepted"}

    def login_proposal_not_yet_accepted(self):
        return self.login_proposal_not_yet_accepted

    def delete_order_success(self):
        return self.delete_order_success

    def order_not_exist(self):
        return self.order_not_exist

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

    def no_file_part(self):
        return self.no_file_part

    def no_selected_file(self):
        return self.no_selected_file

    def upload_successfully(self):
        return self.upload_successfully

    def return_supplier_list(self):
        return self.return_supplier_list

    def supplier_code_existed(self):
        return self.supplier_code_existed

    def supplier_code_invalid(self):
        return self.supplier_code_invalid

    def fail_cheat(self):
        return self.fail_cheat

    def permission_denied(self):
        return self.permission_denied
