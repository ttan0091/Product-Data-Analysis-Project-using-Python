# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import math
import os
import random
import re
import string
import time
import pandas as pd
import matplotlib.pyplot as plt

from model_order import Order
from operation_customer import CustomerOperation
from opreation_product import ProductOperation


class OrderOperation:
    file_path_orders = 'data/orders.txt'
    file_path_figures = 'data/figure'
    file_path_products = 'data/products.txt'
    file_path_users = 'data/users.txt'

    def generate_unique_order_id(self):
        while True:
            order_id = 'o_' + ''.join(random.choices(string.digits, k=5))
            if not self.check_order_id_exist(order_id):
                return order_id

    def create_an_order(self, customer_id, product_id, create_time=None):
        order = self.create_order_object(customer_id, product_id, create_time)
        self.write_order(order)
        return True

    def delete_order(self, order_id):
        # Use the read_orders method with a filter function to exclude the specified order
        orders = self.read_orders(lambda order: order['order_id'] != order_id)

        # Use the write_orders method to write the remaining orders to the file
        self.write_orders(orders)
        return True

    def get_order_list(self, customer_id, page_number):
        # Use the read_orders method with a filter function to get the orders of the specified customer
        orders = self.read_orders(None if customer_id == '' else lambda order: order['user_id'] == customer_id)

        # Set the maximum number of items per page
        items_per_page = 10

        # Calculate the total number of pages
        total_pages = self.get_customer_order_page(customer_id)

        # Get the orders for the requested page
        start_index = page_number * items_per_page
        end_index = start_index + items_per_page
        orders_page = orders[start_index:end_index]

        return orders_page, page_number, total_pages

    def generate_test_order_data(self):
        # Check if the products file is empty, if so, generate products
        if os.stat(self.file_path_products).st_size == 0:
            ProductOperation().extract_products_from_files()

        # Check if the products and orders files exist
        if not os.path.exists(self.file_path_products) or not os.path.exists(self.file_path_orders):
            return

        with open(self.file_path_products, 'r', encoding='utf-8') as file:
            products = [eval(line.strip()) for line in file]
        # Generate 10 customers
        i = 1
        while True:
            letters = string.ascii_lowercase
            username = ''.join(random.choice(letters) for _ in range(5))
            password = 'a0000'
            email = f'{str(i).zfill(10)}@gmail.com'
            mobile = f'03{str(i).zfill(8)}'
            success = CustomerOperation().register_customer(username, password, email, mobile)

            if success:
                i += 1
            if i > 10:
                break

        # from users.txt get 10 customer id
        with open(self.file_path_users, 'r', encoding='utf-8') as file:
            users = [eval(line.strip()) for line in file]
        customers_ids = [user['user_id'] for user in users if user['user_role'] == 'customer']

        # write order to orders.txt
        for customer_id in customers_ids:
            order_count = random.randint(50, 200)
            for _ in range(order_count):
                order_id = self.generate_unique_order_id()

                # Generate a random order time within the past year
                end = time.time()
                start = end - 365 * 24 * 60 * 60
                order_time = start + random.randint(0, int(end - start))

                # Convert the order time to a string in the format 'yyyy-mm-dd hh:mm:ss'
                order_time = time.strftime('%d-%m-%Y_%H:%M:%S', time.localtime(order_time))

                # Select a random product for this order
                product = random.choice(products)

                # Create a new order and write it to the file
                order = Order(order_id, customer_id, product['pro_id'], order_time)
                self.write_order(order)

    def generate_single_customer_consumption_figure(self, customer_id):
        # Get orders with prices
        orders = self.get_orders_and_prices(customer_id)

        # If the customer has no order
        if len(orders) == 0:
            return

        # Create a DataFrame
        df = pd.DataFrame(orders)

        # Group by month and sum the order price
        monthly_consumption = df.groupby('month')['order_price'].sum()

        # Plot
        monthly_consumption.plot(kind='bar', figsize=(10, 5))
        plt.title('Monthly Consumption of Customer {}'.format(customer_id))
        plt.xlabel('Month')
        plt.ylabel('Consumption')
        plt.savefig('data/figure/single_customer_consumption.png')
        plt.close()

    def generate_all_customers_consumption_figure(self):
        # Get orders
        orders = self.get_orders_and_prices()

        # If there is no order
        if len(orders) == 0:
            return

        # Create a DataFrame
        df = pd.DataFrame(orders)

        # Group by month and sum the order price
        monthly_consumption = df.groupby('month')['order_price'].sum()

        # Plot
        monthly_consumption.plot(kind='bar', figsize=(10, 5))
        plt.title('Monthly Consumption of All Customers')
        plt.xlabel('Month')
        plt.ylabel('Consumption')
        plt.savefig('data/figure/all_customers_consumption.png')
        plt.close()

    def generate_all_top_10_best_sellers_figure(self):
        # Check if the orders file exists
        if not os.path.exists(self.file_path_orders):
            return

        # Read the orders file
        with open(self.file_path_orders, 'r', encoding='utf-8') as file:
            orders = [eval(line.strip()) for line in file]

        # Create a DataFrame
        df = pd.DataFrame(orders)

        # Group by product and count the number of orders
        product_counts = df['pro_id'].value_counts().head(10)

        # Plot
        product_counts.plot(kind='bar', figsize=(10, 5))
        plt.title('Top 10 Best-Selling Products')
        plt.xlabel('Product ID')
        plt.ylabel('Number of Orders')
        plt.savefig('data/figure/all_top_10_best_sellers.png')
        plt.close()

    def delete_all_orders(self):
        # Check if the orders file exists
        if not os.path.exists(self.file_path_orders):
            return

        # Open the file in write mode, which will erase all existing data
        with open(self.file_path_orders, 'w', encoding='utf-8') as file:
            pass  # Do nothing, just open the file in write mode to erase all data

    def get_total_order_page(self):
        if not os.path.exists(self.file_path_orders):
            return 0

        page_size = 10
        with open(self.file_path_orders, 'r', encoding='utf-8') as file:
            total_lines = len(file.readlines())

        total_pages = math.ceil(total_lines / float(page_size))
        return total_pages

    # Read orders from file and return a list of all orders
    # A filter function can be passed in to get orders that meet specific conditions
    def read_orders(self, filter_func=None):
        if not os.path.exists(self.file_path_orders):
            return []

        with open(self.file_path_orders, 'r', encoding='utf-8') as file:
            orders = [eval(line.strip()) for line in file]

        if filter_func is not None:
            orders = [order for order in orders if filter_func(order)]

        return orders

    # Create a new order object
    def create_order_object(self, customer_id, product_id, create_time=None):
        create_time = create_time or time.strftime("%d-%m-%Y_%H:%M:%S", time.localtime())
        order_id = self.generate_unique_order_id()
        return Order(order_id, customer_id, product_id, create_time)

    # Write order to file,using append mode
    def write_order(self, order):
        with open(self.file_path_orders, 'a', encoding='utf-8') as file:
            file.write(str(order) + '\n')

    # Write orders to file, using write mode
    def write_orders(self, orders):
        with open(self.file_path_orders, 'w', encoding='utf-8') as file:
            for order in orders:
                file.write(str(order) + '\n')

    # Get the total order pages of one single customer
    def get_customer_order_page(self, customer_id):
        # Use the read_orders method with a filter function to get the orders of the specified customer
        orders = self.read_orders(None if customer_id == '' else lambda order: order['user_id'] == customer_id)

        page_size = 10
        total_lines = len(orders)
        total_pages = math.ceil(total_lines / page_size)
        return total_pages

    # Check if the order id exists
    def check_order_id_exist(self, order_id):
        orders = self.read_orders()
        return any(order['order_id'] == order_id for order in orders)

    # Get a list of orders and their prices for a specific customer
    def get_orders_and_prices(self, customer_id=None):
        # Check if the orders and products files exist
        if not os.path.exists(self.file_path_orders) or not os.path.exists(self.file_path_products):
            return []

        # Read the products file
        with open(self.file_path_products, 'r', encoding='utf-8') as file:
            products = {product['pro_id']: product for product in (eval(line.strip()) for line in file)}

        # Read the orders file
        with open(self.file_path_orders, 'r', encoding='utf-8') as file:
            orders = [eval(line.strip()) for line in file]

        # Filter the orders of the specified customer if customer_id is provided
        if customer_id is not None:
            orders = [order for order in orders if order['user_id'] == customer_id]

        # Add order price to each order
        for order in orders:
            order['order_price'] = float(products[order['pro_id']]['pro_current_price'])
            order['month'] = time.strptime(order['order_time'], "%d-%m-%Y_%H:%M:%S").tm_mon

        return orders

    def validate_order_id(self, order_id):
        pattern = r'^o_\d{5}$'
        if re.match(pattern, order_id):
            return True
        else:
            return False



