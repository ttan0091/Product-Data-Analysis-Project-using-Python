# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import math
import os
import re

from model_customer import Customer
from operation_user import UserOperation


class CustomerOperation(UserOperation):
    file_path_users = 'data/users.txt'

    def validate_email(self, user_email):
        pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
        if not re.match(pattern, user_email):
            return False
        else:
            return True

    def validate_mobile(self, user_mobile):
        pattern = r'^04\d{8}$|^03\d{8}$'
        if not re.match(pattern, user_mobile):
            return False
        else:
            return True

    def register_customer(self, user_name, user_password, user_email, user_mobile):
        # Validate the user input
        if not (self.validate_email(user_email)
                and self.validate_mobile(user_mobile)
                and self.validate_username(user_name)
                and self.validate_password(user_password)):
            return False

        users = self.load_users()

        # Check if the username exists
        if any(user_dict.get('user_name') == user_name for user_dict in users):
            return False

        # Register a new customer
        user_id = self.generate_unique_user_id()
        user_password = self.encrypt_password(user_password)
        new_customer = Customer(
            user_id=user_id,
            user_name=user_name,
            user_password=user_password,
            user_email=user_email,
            user_mobile=user_mobile,
        )
        # Write the customer information to the file
        return self.add_customer_to_file(new_customer)

    def update_profile(self, attribute_name, value, customer_object):
        # Check if the attribute exists and the value is valid
        if attribute_name not in customer_object.__dict__ or not self.validate_user(attribute_name, value):
            return False

        # Update the attribute
        if attribute_name == 'user_password':
            value = self.encrypt_password(value)

        customer_object.__dict__[attribute_name] = value
        self.substitute_customer_to_file(customer_object)
        return True

    def delete_customer(self, customer_id):
        users = self.load_users()

        # Filter out the customer to be deleted
        users = [user for user in users if user.get('user_id') != customer_id]

        # Write the updated users to the file
        return self.write_customers_to_file(users)

    def get_customer_list(self, page_number):
        lines = self.get_all_lines()
        page_size = 10
        customers = []
        total_lines = 0

        for line in lines:
            try:
                dict_customer = eval(line.strip())
            except Exception:
                continue
            if dict_customer['user_role'] == 'customer':
                total_lines += 1
                if (page_number - 1) * page_size < total_lines <= page_number * page_size:
                    customers.append(self.dict_to_customer(dict_customer))

        total_pages = self.get_total_pages()
        return customers, page_number, total_pages

    def delete_all_customers(self):
        lines = self.get_all_lines()
        with open(self.file_path_users, 'w', encoding='utf-8') as file:
            for line in lines:
                try:
                    user_data = eval(line.strip())
                except Exception:
                    continue
                if user_data['user_role'] != 'customer':
                    file.write(line)

    # add a new customer to the file,using 'a' model
    def add_customer_to_file(self, customer):
        try:
            with open(self.file_path_users, 'a', encoding='utf-8') as file:
                file.write(str(customer) + '\n')
        except IOError:
            return False
        return True

    # transform the dict to customer object
    def dict_to_customer(self, dict_customer):
        return Customer(user_id=dict_customer['user_id'],
                        user_name=dict_customer['user_name'],
                        user_password=dict_customer['user_password'],
                        user_register_time=dict_customer['user_register_time'],
                        user_role=dict_customer['user_role'],
                        user_email=dict_customer['user_email'],
                        user_mobile=dict_customer['user_mobile'])

    # Substitute the customer to the file,using 'w' model
    def substitute_customer_to_file(self, customer):
        if not os.path.exists(self.file_path_users):
            return
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            lines = file.readlines()
        with open(self.file_path_users, 'w', encoding='utf-8') as file:
            for line in lines:
                try:
                    user_data = eval(line.strip())
                except Exception:
                    continue
                if user_data['user_id'] == customer.user_id:
                    line = str(customer) + '\n'
                file.write(line)

    # Generate a list of dict for all users from file
    def load_users(self):
        if os.path.exists(self.file_path_users):
            with open(self.file_path_users, 'r', encoding='utf-8') as file:
                return [eval(line.strip()) for line in file]
        return []

    # Get all lines from file, return type is list of str
    def get_all_lines(self):
        if not os.path.exists(self.file_path_users):
            return []
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            return file.readlines()

    # Get the total pages of customers
    def get_total_pages(self):
        lines = self.get_all_lines()
        total_lines = 0
        for line in lines:
            try:
                dict_customer = eval(line.strip())
            except Exception:
                continue
            if dict_customer['user_role'].lower() == 'customer':
                total_lines += 1
        total_pages = math.ceil(total_lines / 10)
        return total_pages

    # Write the list of customers to the file
    def write_customers_to_file(self, users):
        try:
            with open(self.file_path_users, 'w', encoding='utf-8') as file:
                for user in users:
                    file.write(str(user) + '\n')
            return True
        except IOError:
            return False

    # Validate customer id
    def validate_customer_id(self, user_id):
        pattern = r'^u_\d{10}$'
        if re.match(pattern, user_id):
            return True
        else:
            return False

    # Validate customer name or password or email or mobile
    def validate_user(self, attribute_name, value):
        if attribute_name == 'user_email':
            return self.validate_email(value)
        elif attribute_name == 'user_mobile':
            return self.validate_mobile(value)
        elif attribute_name == 'user_name':
            return self.validate_username(value)
        elif attribute_name == 'user_password':
            return self.validate_password(value)
        return False
