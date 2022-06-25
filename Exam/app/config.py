import os

SECRET_KEY='299c02dd1e051ca50ebfa7b0e64e4543ec4c611be7dd430caaecabebaf35e702'
ADMIN_ROLE_ID = 3
SQLALCHEMY_DATABASE_URI = f"mysql+mysqlconnector://std_1685_exam:11111112@std-mysql.ist.mospolytech.ru/std_1685_exam"
SQLALCHEMY_TRACK_MODIFICATIONS = False
SQLALCHEMY_ECHO = True

UPLOAD_FOLDER = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'media', 'images')