# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
import time


class User:
    def __init__(self, user_id='u_0000000000', user_name='', user_password='',
                 user_register_time='00-00-0000_00:00:00', user_role='customer'):
        self.user_id = user_id
        self.user_name = user_name
        self.user_password = user_password
        # The time string should be in the format: "DD-MM-YYYY_HH:MM:SS"
        if user_register_time == '00-00-0000_00:00:00':
            self.user_register_time = time.strftime('%d-%m-%Y_%H:%M:%S', time.localtime())
        else:
            self.user_register_time = user_register_time
        self.user_role = user_role

    def __str__(self):
        return f"{{'user_id':'{self.user_id}', 'user_name':'{self.user_name}', 'user_password':'{self.user_password}', 'user_register_time':'{self.user_register_time}', 'user_role':'{self.user_role}'}}"
