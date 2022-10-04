import os

SECRET_KEY='001ed167aa623cf58f74f6156012c862c0ed26bd39d5fac62f578f5aad84c637'
ADMIN_ROLE_ID = 2
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://std_1685_lab6:11111112@std-mysql.ist.mospolytech.ru/std_1685_lab6"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')