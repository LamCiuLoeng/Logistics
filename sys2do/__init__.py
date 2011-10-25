# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from flask import Flask, Module

__all__ = ["app"]

app = Flask(__name__, static_path = '/static')
app.config.from_object("sys2do.setting")

#if not app.debug:
#    import logging
#    from themodule import TheHandlerYouWant
#    file_handler = TheHandlerYouWant(...)
#    file_handler.setLevel(logging.WARNING)
#    app.logger.addHandler(file_handler)

if app.config.get("LOGGING_FILE", True):
    import logging, logging.handlers
    file_handler = logging.handlers.TimedRotatingFileHandler(app.config.get("LOGGING_FILE_PATH"), when = 'D', interval = 1, backupCount = 5, encoding = "utf-8", delay = False)
    file_handler.setLevel(app.config.get("LoGGING_LEVEL"))
    file_handler.setFormatter(logging.Formatter('''
    Message type:       %(levelname)s
    Location:           %(pathname)s:%(lineno)d
    Function:           %(funcName)s
    Time:               %(asctime)s
    Message:            %(message)s
    '''))
    app.logger.addHandler(file_handler)

#===============================================================================
# sys.py
#===============================================================================
import views.sys as s
for error_code in [403, 404, 500] : app.error_handlers[error_code] = s.error_page(error_code)


#===============================================================================
# root.py
#===============================================================================
import views.root as r
app.add_url_rule("/", view_func = r.index, methods = ['GET', 'POST'])
app.add_url_rule("/index", view_func = r.index, methods = ['GET', 'POST'])






#===============================================================================
# import the customize filter and testing
#===============================================================================
import util.filters as filters
for f in filters.__all__ : app.jinja_env.filters[f] = getattr(filters, f)

import util.tests as tests
for t in tests.__all__ : app.jinja_env.tests[t] = getattr(tests, t)
