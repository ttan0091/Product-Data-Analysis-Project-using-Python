# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
class Product:
    def __init__(self, pro_id='', pro_model='', pro_category='', pro_name='',
                 pro_current_price=0.0, pro_raw_price=0.0, pro_discount=0.0, pro_likes_count=0):
        self.pro_id = pro_id
        self.pro_model = pro_model
        self.pro_category = pro_category
        self.pro_name = pro_name
        self.pro_current_price = pro_current_price
        self.pro_raw_price = pro_raw_price
        self.pro_discount = pro_discount
        self.pro_likes_count = pro_likes_count

    # def __str__(self):
    #     return "{'pro_id':'{}', 'pro_model':'{}', 'pro_category':'{}', 'pro_name':'{}', \
    # 'pro_current_price':'{}', 'pro_raw_price':'{}', 'pro_discount':'{}', 'pro_likes_count':'{}'}".format(
    #         self.pro_id,
    #         self.pro_model,
    #         self.pro_category,
    #         self.pro_name.replace("'", "''").replace('"', '""'),
    #         self.pro_current_price,
    #         self.pro_raw_price,
    #         self.pro_discount,
    #         self.pro_likes_count
    #     )
    def __str__(self):
        return "{{'pro_id':'{}', 'pro_model':'{}', 'pro_category':'{}', 'pro_name':'{}', \
    'pro_current_price':'{}', 'pro_raw_price':'{}', 'pro_discount':'{}', 'pro_likes_count':'{}'}}".format(
            self.pro_id,
            self.pro_model,
            self.pro_category,
            self.pro_name.replace("'", "\\'").replace('"', '\\"'),
            self.pro_current_price,
            self.pro_raw_price,
            self.pro_discount,
            self.pro_likes_count
        )
