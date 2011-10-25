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

#upload setting
UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), "static", "upload")
UPLOAD_FOLDER_URL = "/static/upload"
ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif', 'doc'])


#session setting
SECRET_KEY = str(uuid.uuid4())
USE_X_SENDFILE = False
SERVER_NAME = None
MAX_CONTENT_LENGTH = None
TESTING = False
PERMANENT_SESSION_LIFETIME = datetime.timedelta(days = 31)
SESSION_COOKIE_NAME = 'session'



#config for logging
LOGGING_FILE = True
LOGGING_FILE_PATH = os.path.join(os.path.dirname(__file__), "..", "system_log.txt")
LoGGING_LEVEL = logging.INFO


#database setting
#sqlite
SQLALCHEMY_DATABASE_URI = 'sqlite:///%s' % (os.path.join(os.path.dirname(__file__), ".." , "logistics.db"))
#mysql
#SQLALCHEMY_DATABASE_URI = sqlalchemy.url=mysql://username:password@hostname:port/databasename
#postgresql
#SQLALCHEMY_DATABASE_URI = sqlalchemy.url=postgresql://postgres:admin@hostname:port/databasename
