# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import os, datetime, uuid, logging

DEBUG = True

# upload setting
UPLOAD_FOLDER_PREFIX = os.path.dirname(__file__)
UPLOAD_FOLDER = os.path.join("static", "upload")
UPLOAD_FOLDER_URL = "/static/upload"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])


TMP_FOLDER = os.path.join(os.path.dirname(__file__), "static", "tmp")
TEMPLATE_FOLDER = os.path.join(os.path.dirname(__file__), "static", "template")

# session setting

SECRET_KEY = str(uuid.uuid4())
USE_X_SENDFILE = False
SERVER_NAME = None
MAX_CONTENT_LENGTH = None
TESTING = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days = 31)
SESSION_COOKIE_NAME = 'session'



# Beaker session setting
BEAKER_SESSION = {
                  'session.type': 'file',
                  'session.data_dir': os.path.join(os.path.dirname(__file__), "session", "data"),
                  'session.lock_dir': os.path.join(os.path.dirname(__file__), "session", "lock"),
                  }


# config for logging
LOGGING_FILE = True
LOGGING_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "system_log.txt")
LOGGING_LEVEL = logging.DEBUG



# config for i18n
BABEL_DEFAULT_LOCALE = 'zh_CN'
BABEL_DEFAULT_TIMEZONE = 'UTC'

# database setting
# sqlite
# SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(os.path.dirname(__file__), ".." , "logistics.db"))
# mysql
# SQLALCHEMY_DATABASE_URI = sqlalchemy.url=mysql://username:password@hostname:port/databasename
# SQLALCHEMY_DATABASE_URI = 'mysql://root:admin@192.168.21.157:3306/logistics'
# postgresql
SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:admin@192.168.21.157:5433/aa'



# setting for paginate ,every page is 20 recore
PAGINATE_PER_PAGE = 20


# sessing for SMS
SMS_KEY = 'af60848fc19ee0866e376eb60c55e969'
SMS_FORMAT = u'%s[深福合力]'
