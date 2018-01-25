import os

BASE_DIR = os.path.abspath('.')

DEBUG = False
TESTING = False
PRESERVE_CONTEXT_ON_EXCEPTION = False

# Конфиг для бд
SQLALCHEMY_DATABASE_URI = 'postgresql://username:password@localhost/pass_service'

SQLALCHEMY_TRACK_MODIFICATIONS = False

from config_local import *
