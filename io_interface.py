# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import pandas as pd

from operation_customer import CustomerOperation


class IOInterface:
    def get_user_input(self, message, num_of_args):
        user_input = input(message).split()[:num_of_args]
        user_input += [''] * (num_of_args - len(user_input))  # Append empty strings if necessary
        return user_input

    def main_menu(self):
        print("\n---------Main Menu---------------------------")
        print("         (1) Login")
        print("         (2) Register")
        print("         (3) Quit")

    def admin_menu(self):
        print("\n---------Admin Menu---------------------------")
        print("         (1) Show products")
        print("         (2) Add customers")
        print("         (3) Show customers")
        print("         (4) Show orders")
        print("         (5) Generate test data")
        print("         (6) Generate all statistical figures")
        print("         (7) Delete all data")
        print("         (8) Delete customer using customer id")
        print("         (9) Delete order using order id")
        print("         (10) Delete product using product id")
        print("         (11) Logout")

    def customer_menu(self):
        print("\n---------Customer Menu------------------------")
        print("         (1) Show profile")
        print("         (2) Update profile")
        print("         (3) Show products")
        print("         (4) Show history orders")
        print("         (5) Generate all consumption figures")
        print("         (6) Get product using product id")
        print("         (7) Logout")

    def show_list(self, user_role, list_type, object_list):
        user_role = user_role.lower()
        list_type = list_type.lower()

        if user_role not in ['admin', 'customer']:
            print("Invalid role!")
            return
        if list_type not in ['customer', 'product', 'order']:
            print("Invalid list type!")
            return
        if user_role == 'customer' and list_type == 'customer':
            print("Customer cannot view customer list!")
            return

        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        items, page_number, total_page = object_list
        items_dict = [eval(str(item)) for item in items]
        df = pd.DataFrame(items_dict)
        df.reset_index(drop=True, inplace=True)
        df.index = df.index + 1

        if df.empty:
            print("No data!")
        else:
            print(f"-------------------------------- {list_type} List --------------------------------")
            print(df)

        print(f"Page: {page_number} of {total_page}\n")

    def show_list_by_object(self, items):
        pd.set_option('display.max_rows', None)
        pd.set_option('display.max_columns', None)
        pd.set_option('display.expand_frame_repr', False)
        items_dict = [eval(str(item)) for item in items]
        df = pd.DataFrame(items_dict)
        df.reset_index(drop=True, inplace=True)
        df.index = df.index + 1

        if df.empty:
            print("No data!")
        else:
            print(df)

    def print_error_message(self, error_source, error_message):
        print("Error {}: {}".format(error_source, error_message))

    def print_message(self, message):
        print(message)

    def print_object(self, target_object):
        print(str(target_object))

    def get_input_customer_details(self):
        customer_operation = CustomerOperation()
        while True:
            customer_name = input("Please enter your new name(No less than 5 characters): ")
            if customer_operation.validate_username(customer_name):
                break
            else:
                self.print_message("Invalid username. Please try again.")
        while True:
            customer_password = input("Please enter the customer password: ")
            if customer_operation.validate_password(customer_password):
                break
            else:
                self.print_message("Invalid password. Please try again.")
        while True:
            customer_email = input("Please enter the customer email: ")
            if customer_operation.validate_email(customer_email):
                break
            else:
                self.print_message("Invalid email. Please try again.")
        while True:
            customer_mobile = input("Please enter the customer mobile(start with 03 or 04, length 10 total): ")
            if customer_operation.validate_mobile(customer_mobile):
                break
            else:
                self.print_message("Invalid mobile. Please try again.")

        return customer_name, customer_password, customer_email, customer_mobile
