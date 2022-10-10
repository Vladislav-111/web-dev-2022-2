from flask_login import current_user
from app import app

def is_admin():
    return current_user.role_id == app.config.get('ADMIN_ROLE_ID')

def is_moderator():
    return current_user.role_id == app.config.get('MODER_ROLE_ID')


class UsersPolicy:
    def __init__(self, role_id):
        self.role_id = role_id
    
    def create(self):
        return is_admin()

    def delete(self):
        return is_admin()

    def update(self):
        return is_admin() or is_moderator()
