# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1

class Order:
    def __init__(self, order_id='o_00000', user_id='', pro_id='',
                 order_time='00-00-0000_00:00:00'):
        self.order_id = order_id
        self.user_id = user_id
        self.pro_id = pro_id
        self.order_time = order_time

    def __str__(self):
        return f"{{'order_id':'{self.order_id}', 'user_id':'{self.user_id}', \
'pro_id':'{self.pro_id}', 'order_time':'{self.order_time}'}}"
