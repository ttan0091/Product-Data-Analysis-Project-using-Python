# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
from io_interface import IOInterface
from model_admin import Admin
from model_customer import Customer
from operation_admin import AdminOperation
from operation_customer import CustomerOperation
from operation_user import UserOperation
from operation_order import OrderOperation
from opreation_product import ProductOperation


def login_control(ioi, user_operation):
    while True:
        username, password = ioi.get_user_input(
            "Please enter your username(>=5 characters)\n"
            "and password(>=5 characters, alphabet and number contained),separated with whitespace : ",
            2)

        # validate username and password
        if not user_operation.validate_username(username):
            ioi.print_error_message("UserOperation.validate", "Username format incorrect")
            continue
        if not user_operation.validate_password(password):
            ioi.print_error_message("UserOperation.validate", "Password format incorrect")
            continue

        # login
        user_role = user_operation.login(username, password)
        if user_role is not None:
            return user_role
        else:
            ioi.print_error_message("UserOperation.login", "Username or password incorrect")


def customer_control(ioi, customer_obj, customer_operation, order_operation, product_operation):
    ioi.print_message(f"Welcome {customer_obj.user_name}!")
    while True:
        ioi.customer_menu()
        i = ioi.get_user_input("Please enter your choice: ", 1)[0]
        if i == '1':
            # show customer info
            ioi.show_list_by_object([customer_obj])

        elif i == '2':
            # update customer info
            ioi.print_message("user_name:1\nuser_password:2\nuser_email:3\nuser_mobile:4\n")
            input_num = ioi.get_user_input("Please enter the attribute number above you want to update: ", 1)[0]
            attribute, value = '', ''
            if input_num == '1':
                attribute = 'user_name'
                while True:
                    new_name = ioi.get_user_input("Please enter your new name(longer than 5 characters): ", 1)[0]
                    if customer_operation.validate_username(new_name):
                        value = new_name
                        break
                    else:
                        ioi.print_error_message("UserOperation.validate_username", "Username format incorrect")
            elif input_num == '2':
                attribute = 'user_password'
                while True:
                    new_password = ioi.get_user_input("Please enter your new password: ", 1)[0]
                    if customer_operation.validate_password(new_password):
                        value = new_password
                        break
                    else:
                        ioi.print_error_message("UserOperation.validate_password", "Password format incorrect")
            elif input_num == '3':
                attribute = 'user_email'
                while True:
                    new_email = ioi.get_user_input("Please enter your new email: ", 1)[0]
                    if customer_operation.validate_email(new_email):
                        value = new_email
                        break
                    else:
                        ioi.print_error_message("CustomerOperation.validate_email", "Email format incorrect")
            elif input_num == '4':
                attribute = 'user_mobile'
                while True:
                    new_mobile = ioi.get_user_input("Please enter your new mobile(start with 03 or 04, length 10 "
                                                    "total): ", 1)[0]
                    if customer_operation.validate_mobile(new_mobile):
                        value = new_mobile
                        break
                    else:
                        ioi.print_error_message("CustomerOperation.validate_mobile", "Mobile format incorrect")
            else:
                ioi.print_error_message("Input", "Input should between 1-4")
                continue

            customer_operation.update_profile(attribute, value, customer_obj)
            ioi.print_message("Update successfully!")
            ioi.print_message(f"Your new {attribute} is {value}")

        elif i == '3':
            # show products
            keyword_or_page = ioi.get_user_input("Enter 1 to search by keyword, 2 to search by page number: ", 1)[0]
            if keyword_or_page == '1':
                keyword = ioi.get_user_input("Please enter the keyword you want to search: ", 1)[0]
                ioi.print_message(f"Searching result for {keyword}...")
                products = product_operation.get_product_list_by_keyword(keyword)
                ioi.show_list_by_object(products)

            elif keyword_or_page == '2':
                total_page = product_operation.get_total_pages()
                page = ioi.get_user_input(f"Enter page number between 1 and {total_page} to see the products: ", 1)[0]

                if not page.isdigit():
                    ioi.print_error_message("Input", "Input should be a number.")
                elif int(page) < 1 or int(page) > total_page:
                    ioi.print_error_message("Input", "Input should between 1 and total page number.")
                else:
                    ioi.print_message(f"Searching result for page {page}...")
                    product_list = product_operation.get_product_list(int(page))
                    ioi.show_list('customer', 'product', product_list)
            else:
                ioi.print_error_message("Input", "Input should be 1 or 2.")

        elif i == '4':
            # show orders
            customer_id = customer_obj.__dict__['user_id']
            total_page = order_operation.get_customer_order_page(customer_id)
            if total_page == 0:
                ioi.print_message("No data!")
                continue

            page = ioi.get_user_input(f"Enter page number between 1 and {total_page} to see the orders: ", 1)[0]
            if not page.isdigit():
                ioi.print_error_message("Input", "Input should be a number.")
            elif int(page) < 1 or int(page) > total_page:
                ioi.print_error_message("Input", "Input should between 1 and total page number.")
            else:
                order_list = order_operation.get_order_list(customer_id, int(page))
                ioi.show_list('customer', 'order', order_list)

        elif i == '5':
            # generate figure
            customer_id = customer_obj.__dict__['user_id']
            ioi.print_message("Generating figure...")
            order_operation.generate_single_customer_consumption_figure(customer_id)
            ioi.print_message("Figure generated successfully!")
            ioi.print_message("Figures will show up in data/figure within 3 minutes.")
        elif i == '6':
            # get product using product id
            product_id = ioi.get_user_input("Please enter the product id you want to see: ", 1)[0]
            product = product_operation.get_product_by_id(product_id)
            if product:
                ioi.show_list_by_object([product])
            else:
                ioi.print_error_message("ProductOperation.get_product_by_id", "Product not found.")

        elif i == '7':
            # log out
            break
        else:
            ioi.print_error_message("Input", "Input should between 1-6.")


def admin_control(ioi, admin_operation, customer_operation, order_operation, product_operation):
    ioi.print_message("\nWelcome to admin control panel.")
    while True:
        ioi.admin_menu()
        i = ioi.get_user_input("Please enter your choice: ", 1)[0]
        if i == '1':
            # show product list
            total_pages = product_operation.get_total_pages()
            if total_pages == 0:
                ioi.print_message("No data!")
                continue

            page = ioi.get_user_input(f"Enter page number between 1 and {total_pages} to see the products: ", 1)[0]
            if not page.isdigit():
                ioi.print_error_message("Input", "Input should be a number.")
            elif int(page) < 1 or int(page) > total_pages:
                ioi.print_error_message("Input", "Input should between 1 and total page number.")
            else:
                product_list = product_operation.get_product_list(int(page))
                ioi.show_list('admin', 'product', product_list)

        elif i == '2':
            # Register customer
            customer_name, customer_password, customer_email, customer_mobile = ioi.get_input_customer_details()

            success = customer_operation.register_customer(customer_name, customer_password, customer_email,
                                                           customer_mobile)
            if success:
                ioi.print_message("Register successfully!")
            else:
                ioi.print_error_message("customer_operation.register_customer", "Register failed.")

        elif i == '3':
            # show customer list
            page_total = customer_operation.get_total_pages()
            if page_total == 0:
                ioi.print_message("No data!")
                continue

            page = ioi.get_user_input(f"Enter page number between 1 and {page_total} to see the customers: ", 1)[0]
            if not page.isdigit():
                ioi.print_error_message("Input", "Input should be a number.")
            elif int(page) < 1 or int(page) > page_total:
                ioi.print_error_message("Input", "Input should between 1 and total page number.")
            else:
                customer_list = customer_operation.get_customer_list(int(page))
                ioi.show_list('admin', 'customer', customer_list)

        elif i == '4':
            # show order list
            page_total = order_operation.get_total_order_page()
            if page_total == 0:
                ioi.print_message("No data!")
                continue

            page = ioi.get_user_input(f"Enter page number between 1 and {page_total} to see the orders: ", 1)[0]
            if not page.isdigit():
                ioi.print_error_message("Input", "Input should be a number.")
            elif int(page) < 1 or int(page) > page_total:
                ioi.print_error_message("Input", "Input should between 1 and total page number.")
            else:
                order_list = order_operation.get_order_list('', int(page))
                ioi.show_list('admin', 'order', order_list)

        elif i == '5':
            # generate test data
            ioi.print_message("Generating data, please wait...")
            order_operation.generate_test_order_data()
            ioi.print_message("Products/orders/users data generated successfully.")

        elif i == '6':
            # generate figures
            ioi.print_message("Generating figures, please wait...")
            order_operation.generate_all_customers_consumption_figure()
            order_operation.generate_all_top_10_best_sellers_figure()
            product_operation.generate_category_figure()
            product_operation.generate_discount_likes_count_figure()
            product_operation.generate_likes_count_figure()
            product_operation.generate_discount_figure()
            ioi.print_message("Figures generated successfully.")
            ioi.print_message("Figures will show up in data/figure within 3 minutes.")

        elif i == '7':
            # delete data
            ioi.print_message("1. Delete all users")
            ioi.print_message("2. Delete all orders")
            ioi.print_message("3. Delete all products")
            ioi.print_message("4. Delete all the data above")
            selection = ioi.get_user_input("Enter a number to delete data:", 1)[0]
            if selection == '1':
                customer_operation.delete_all_customers()
                admin_operation.delete_admin_account()
                ioi.print_message("All users deleted.")
            elif selection == '2':
                order_operation.delete_all_orders()
                ioi.print_message("All orders deleted.")
            elif selection == '3':
                product_operation.delete_all_products()
                ioi.print_message("All products deleted.")
            elif selection == '4':
                customer_operation.delete_all_customers()
                admin_operation.delete_admin_account()
                order_operation.delete_all_orders()
                product_operation.delete_all_products()
                ioi.print_message("All data deleted.")
            else:
                ioi.print_error_message("Input", "Input should between 1 and 4.")

        elif i == '8':
            # Delete customer using customer id
            customer_id = ioi.get_user_input("Enter customer id to delete(format:u_0000000000): ", 1)[0]
            if not customer_operation.validate_customer_id(customer_id):
                ioi.print_error_message("Customer_operation.validate_customer_id", "Invalid customer id.")
            else:
                success = customer_operation.delete_customer(customer_id)
                if success:
                    ioi.print_message("Customer deleted successfully!")
                else:
                    ioi.print_error_message("Customer_operation.delete_customer", "Customer_id not exist.")

        elif i == '9':
            # delete order using order id
            order_id = ioi.get_user_input("Enter order id to delete(format:o_00000): ", 1)[0]
            if not order_operation.validate_order_id(order_id):
                ioi.print_error_message("Order_operation.validate_order_id", "Invalid order id.")
            else:
                success = order_operation.delete_order(order_id)
                if success:
                    ioi.print_message("Order deleted successfully!")
                else:
                    ioi.print_error_message("Order_operation.delete_order", "Order_id not exist.")

        elif i == '10':
            # delete product using product id
            product_id = ioi.get_user_input("Enter product id to delete: ", 1)[0]
            success = product_operation.delete_product(product_id)
            if success:
                ioi.print_message("Product deleted successfully!")
            else:
                ioi.print_error_message("Product_operation.delete_product", "Product_id not exist.")

        elif i == '11':
            # logout
            break
        else:
            ioi.print_error_message("Input", "Input should between 1-8.")


def main():
    # create all the objects needed
    ioi = IOInterface()
    user_operation = UserOperation()
    admin_operation = AdminOperation()
    order_operation = OrderOperation()
    product_operation = ProductOperation()
    customer_operation = CustomerOperation()

    # delete all the data in the database for a new program run
    order_operation.delete_all_orders()
    product_operation.delete_all_products()
    customer_operation.delete_all_customers()
    admin_operation.delete_admin_account()

    # register an admin
    admin_operation.register_admin()

    while True:
        ioi.main_menu()
        user_choice = ioi.get_user_input("Enter your choice: ", 1)[0]
        if user_choice == '1':
            user_role = login_control(ioi, user_operation)
            if isinstance(user_role, Admin):
                admin_control(ioi, admin_operation, customer_operation, order_operation, product_operation)
            elif isinstance(user_role, Customer):
                customer_control(ioi, user_role, customer_operation, order_operation, product_operation)
        elif user_choice == '2':
            customer_name, customer_password, customer_email, customer_mobile = ioi.get_input_customer_details()
            success = customer_operation.register_customer(customer_name, customer_password, customer_email,
                                                           customer_mobile)
            if success:
                ioi.print_message("Register successfully")
            else:
                ioi.print_message("Register failed")
        elif user_choice == '3':
            ioi.print_message("Bye!")
            break
        else:
            ioi.print_message("Invalid input. Please try again.")


if __name__ == "__main__":
    main()
