# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import random
import string
import re
import os

from model_admin import Admin
from model_customer import Customer


class UserOperation:
    file_path_users = 'data/users.txt'

    def generate_unique_user_id(self):
        existing_ids = self.get_existing_ids()
        while True:
            # Generate a random 10-digit number and prepend 'u_'
            user_id = 'u_' + ''.join(random.choices('0123456789', k=10))
            if user_id not in existing_ids:
                return user_id

    def get_existing_ids(self):
        if not os.path.exists(self.file_path_users):
            return set()
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        existing_ids = set()

        for line in lines:
            try:
                user_data = eval(line.strip())
                existing_ids.add(user_data['user_id'])
            except Exception:
                continue
        return existing_ids

    def encrypt_password(self, user_password):
        random_string = ''.join(random.choices(string.ascii_letters + string.digits, k=2 * len(user_password)))
        encrypted_password = ''
        for i in range(len(user_password)):
            encrypted_password += random_string[i * 2:i * 2 + 2] + user_password[i]
        return '^^' + encrypted_password + '$$'

    def decrypt_password(self, encrypted_password):
        encrypted_password = encrypted_password[2:-2]
        decrypted_password = ''
        for i in range(2, len(encrypted_password), 3):
            decrypted_password += encrypted_password[i]
        return decrypted_password

    def check_username_exist(self, user_name):
        if not os.path.exists(self.file_path_users):
            return False
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            try:
                user_data = eval(line.strip())
                if user_data['user_name'] == user_name:
                    return True
            except Exception:
                continue
        return False

    def validate_username(self, user_name):
        if len(user_name) < 5:
            return False
        if not re.match("^[A-Za-z_]*$", user_name):
            return False
        return True

    def validate_password(self, user_password):
        if len(user_password) < 5:
            return False
        if not re.search("[a-zA-Z]", user_password):
            return False
        if not re.search("[0-9]", user_password):
            return False
        return True

    def login(self, user_name, user_password):
        if not os.path.exists(self.file_path_users):
            return None
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        for line in lines:
            try:
                user_data = eval(line.strip())
                if user_data['user_name'].upper() == user_name.upper():
                    if self.decrypt_password(user_data['user_password']) == user_password:
                        if user_data['user_role'] == 'customer':
                            return Customer(
                                user_id=user_data['user_id'],
                                user_name=user_name,
                                user_password=user_data['user_password'],
                                user_email=user_data['user_email'],
                                user_mobile=user_data['user_mobile']
                            )
                        else:
                            return Admin(
                                user_name=user_name,
                                user_password=user_password
                            )
            except Exception:
                continue
        return None
