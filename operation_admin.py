# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import os

from model_admin import Admin
from operation_user import UserOperation


class AdminOperation(UserOperation):
    def register_admin(self):
        admin_id = 'a_1234567890'
        admin_name = 'Admin'
        admin_password = 'a0000'

        # Check if the admin already exists.
        if os.path.exists(self.file_path_users):
            with open(self.file_path_users, 'r', encoding='utf-8') as file:
                for line in file:
                    user_dict = eval(line.strip())
                    if user_dict['user_id'] == admin_id:
                        # Admin already exists, no need to register again.
                        return

        # Admin does not exist, register a new admin.
        new_admin = Admin(user_id=admin_id, user_name=admin_name, user_password=self.encrypt_password(admin_password))
        with open(self.file_path_users, 'a', encoding='utf-8') as file:
            file.write(str(new_admin) + '\n')

    def delete_admin_account(self):
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(self.file_path_users, 'w', encoding='utf-8') as file:
            for line in lines:
                user_dict = eval(line.strip())
                if user_dict['user_name'] != 'Admin':
                    file.write(line)