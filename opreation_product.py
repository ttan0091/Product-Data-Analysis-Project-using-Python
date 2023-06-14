# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import math

import matplotlib
import pandas as pd
import os
import matplotlib.pyplot as plt

from model_product import Product


class ProductOperation:
    file_path_products = 'data/products.txt'
    file_path_source = 'data/product'
    file_path_figures = 'data/figure'

    def extract_products_from_files(self):
        # Check if the source directory exists
        if not os.path.exists(self.file_path_source):
            return

        # Get all CSV files in the source directory
        csv_files = [f for f in os.listdir(self.file_path_source) if f.endswith('.csv')]
        # Open the products.txt file in write mode
        with open(self.file_path_products, 'w', encoding='utf-8') as products_file:
            # Iterate over each CSV file
            for csv_file in csv_files:
                file_path = os.path.join(self.file_path_source, csv_file)
                df = pd.read_csv(file_path)  # read CSV file into DataFrame
                for _, row in df.iterrows():
                    product = Product(
                        pro_id=row['id'],
                        pro_model=row['model'],
                        pro_category=row['category'],
                        pro_name=row['name'],
                        pro_current_price=row['current_price'],
                        pro_raw_price=row['raw_price'],
                        pro_discount=row['discount'],
                        pro_likes_count=row['likes_count']
                    )


                    products_file.write(str(product) + '\n')
                    # a += 1  ############
                    # if a == 10:  ############
                    #     return  #############

    def get_product_list(self, page_number):
        try:
            with open(self.file_path_products, 'r', encoding='utf-8') as products_file:
                lines = products_file.readlines()
            total_page = math.ceil(len(lines) / 10)
            page_number -= 1
            start_index = page_number * 10
            end_index = start_index + 10

            page_lines = lines[start_index:end_index]

            product_list = [self.dict_to_product(eval(line.strip())) for line in page_lines]
            return product_list, page_number + 1, total_page
        except FileNotFoundError:
            return [], page_number + 1, 0

    def get_product_list_by_keyword(self, keyword):
        keyword = keyword.lower()

        result = []
        if not os.path.exists(self.file_path_products):
            return result
        with open(self.file_path_products, 'r', encoding='utf-8') as file:
            for line in file:
                # parse the product dict from the line
                product_dict = eval(line.strip())
                # convert product name to lower case and check if it contains the keyword
                if keyword in product_dict['pro_name'].lower():
                    # create a product object from the dict and append to result
                    product = self.dict_to_product(product_dict)
                    result.append(product)
        return result

    def get_product_by_id(self, product_id):

        if not os.path.exists(self.file_path_products):
            return None
        with open(self.file_path_products, 'r', encoding='utf-8') as file:
            for line in file:
                product_dict = eval(line.strip())
                if product_id == product_dict['pro_id']:
                    product = self.dict_to_product(product_dict)
                    return product
        return None

    def generate_product_dataframe(self):
        # create figure directory if not exist
        if not os.path.exists(self.file_path_figures):
            os.makedirs(self.file_path_figures)

        # check if the products file exists
        if not os.path.exists(self.file_path_products):
            return None

        # read products into a DataFrame
        with open(self.file_path_products, 'r', encoding='utf-8') as file:
            data = [eval(line.strip()) for line in file]
        df = pd.DataFrame(data)
        return df

    def generate_category_figure(self):
        df = self.generate_product_dataframe()
        if df is None:
            return

        # calculate the total number of products for each category
        category_counts = df['pro_category'].value_counts()

        # generate the bar chart
        matplotlib.use('agg')
        plt.figure(figsize=(10, 5))
        category_counts.sort_values(ascending=False).plot(kind='bar', color='skyblue')
        plt.title('Total Number of Products for Each Category')
        plt.xlabel('Number of Products')
        plt.ylabel('Category')

        # save the figure into the figures folder
        plt.savefig(os.path.join(self.file_path_figures, 'category_figure.png'))
        plt.close()

    def generate_discount_figure(self):
        df = self.generate_product_dataframe()
        if df is None:
            return

        # convert discount to numeric
        df['pro_discount'] = pd.to_numeric(df['pro_discount'], errors='coerce')

        # create discount categories
        bins = [0, 30, 60, df['pro_discount'].max()]
        labels = ['<30', '30-60', '>60']
        df['discount_category'] = pd.cut(df['pro_discount'], bins=bins, labels=labels)

        # calculate the number of products in each category
        category_counts = df['discount_category'].value_counts()

        # generate the pie chart
        matplotlib.use('agg')
        plt.figure(figsize=(10, 6))
        plt.pie(category_counts, labels=labels, autopct='%1.1f%%')
        plt.title('Proportion of Products by Discount Category')

        # save the figure into the figures folder
        plt.savefig(os.path.join(self.file_path_figures, 'discount_figure.png'))
        plt.close()

    def generate_likes_count_figure(self):
        df = self.generate_product_dataframe()
        if df is None:
            return

        # convert likes_count to numeric
        df['pro_likes_count'] = pd.to_numeric(df['pro_likes_count'], errors='coerce')

        # calculate the total likes for each category
        category_likes = df.groupby('pro_category')['pro_likes_count'].sum().sort_values()

        # generate the bar chart
        matplotlib.use('agg')
        plt.figure(figsize=(10, 5))
        category_likes.plot(kind='bar', color='red')
        plt.title('Total Likes for Each Category')
        plt.xlabel('Total Likes')
        plt.ylabel('Category')

        # save the figure into the figures folder
        plt.savefig(os.path.join(self.file_path_figures, 'likes_count_figure.png'))
        plt.close()

    def generate_discount_likes_count_figure(self):
        df = self.generate_product_dataframe()
        if df is None:
            return
        # convert discount and likes_count to numeric
        df['pro_discount'] = pd.to_numeric(df['pro_discount'], errors='coerce')
        df['pro_likes_count'] = pd.to_numeric(df['pro_likes_count'], errors='coerce')

        # generate the scatter chart
        matplotlib.use('agg')
        plt.figure(figsize=(10, 5))
        plt.scatter(df['pro_discount'], df['pro_likes_count'])
        plt.title('Relationship between Likes Count and Discount')
        plt.xlabel('Discount')
        plt.ylabel('Likes Count')

        # save the figure into the figures folder
        plt.savefig(os.path.join(self.file_path_figures, 'discount_likes_count_figure.png'))
        plt.close()

    def delete_product(self, product_id):
        try:
            with open(self.file_path_products, 'r', encoding='utf-8') as products_file:
                lines = products_file.readlines()
            is_exist = False
            with open(self.file_path_products, 'w', encoding='utf-8') as products_file:
                for line in lines:
                    product_dict = eval(line)
                    if product_dict['pro_id'] != product_id:
                        products_file.write(line)
                    else:
                        is_exist = True
                return is_exist
        except FileNotFoundError:
            return False

    def delete_all_products(self):
        if not os.path.exists(self.file_path_products):
            return
        with open(self.file_path_products, 'w', encoding='utf-8') as file:
            file.write('')

    def get_total_pages(self):
        if not os.path.exists(self.file_path_products):
            return 0
        with open(self.file_path_products, 'r', encoding='utf-8') as file:
            data = [eval(line.strip()) for line in file]
        df = pd.DataFrame(data)
        return math.ceil(df.shape[0] / 10)

    def dict_to_product(self, product_dict):
        return Product(
            pro_id=product_dict['pro_id'],
            pro_model=product_dict['pro_model'],
            pro_category=product_dict['pro_category'],
            pro_name=product_dict['pro_name'],
            pro_current_price=product_dict['pro_current_price'],
            pro_raw_price=product_dict['pro_raw_price'],
            pro_discount=product_dict['pro_discount'],
            pro_likes_count=product_dict['pro_likes_count']
        )


