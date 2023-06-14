# Student ID: 33569479
# Student Name:Tao Tan
# Creation date:2023-5-19
# Last modified date:2023-6-1
from model_user import User


class Customer(User):
    def __init__(self, user_id='u_0000000000', user_name='', user_password='',
                 user_register_time='00-00-0000_00:00:00', user_role='customer',
                 user_email='', user_mobile=''):
        super().__init__(user_id, user_name, user_password, user_register_time, user_role)
        self.user_email = user_email
        self.user_mobile = user_mobile

    def __str__(self):
        base_info = super().__str__().rstrip('}')
        return f"{base_info}, 'user_email':'{self.user_email}', 'user_mobile':'{self.user_mobile}'}}"
