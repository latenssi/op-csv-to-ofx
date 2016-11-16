# config.py

import os

class BaseConfig(object):
    SECRET_KEY = os.environ['SECRET_KEY'] 
    DEBUG = os.environ['DEBUG']
    UPLOAD_FOLDER = os.environ.get('UPLOAD_FOLDER', '/tmp')
    ALLOWED_EXTENSIONS = set(['csv'])
    MAX_CONTENT_LENGTH = 512 * 1024 # 512 KB