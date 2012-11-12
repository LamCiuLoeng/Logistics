# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
from flask import Flask, Module, request
from flaskext.babel import Babel

__all__ = ["app"]

app = Flask(__name__, static_url_path = '/static')
app.config.from_object("sys2do.setting")
babel = Babel(app)


@babel.localeselector
def get_locale():
    return None  # force the system to use the default setting, zh_CN
    return request.accept_languages.best_match(['zh_CN', 'zh_HK', 'en'])



# if not app.debug:
#    import logging
#    from themodule import TheHandlerYouWant
#    file_handler = TheHandlerYouWant(...)
#    file_handler.setLevel(logging.WARNING)
#    app.logger.addHandler(file_handler)

if app.config.get("LOGGING_FILE", True):
    import logging, logging.handlers
    file_handler = logging.handlers.TimedRotatingFileHandler(app.config.get("LOGGING_FILE_PATH"), when = 'D', interval = 1, backupCount = 5, encoding = "utf-8", delay = False)
    file_handler.setLevel(app.config.get("LOGGING_LEVEL"))
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
for error_code in [403, 404, 500] : app.error_handler_spec[None][error_code] = s.error_page(error_code)


#===============================================================================
# root.py
#===============================================================================
# import views.root as r
# app.add_url_rule("/", view_func = r.index, methods = ['GET', 'POST'])
# app.add_url_rule("/index", view_func = r.index, methods = ['GET', 'POST'])



#===============================================================================
# access.py
#===============================================================================
# import views.access as a
# app.add_url_rule("/user", view_func = a.userHandler, methods = ['GET', 'POST'])
# app.add_url_rule("/group", view_func = a.groupHandler, methods = ['GET', 'POST'])
# app.add_url_rule("/permission", view_func = a.permissionHandler, methods = ['GET', 'POST'])

import views.root
app.register_blueprint(views.root.bpRoot)

import views.auth
app.register_blueprint(views.auth.bpAuth, url_prefix = '/auth')

import views.admin
app.register_blueprint(views.admin.bpAdmin, url_prefix = '/admin')

import views.master
app.register_blueprint(views.master.bpMaster, url_prefix = '/master')

import views.order
app.register_blueprint(views.order.bpOrder, url_prefix = '/order')

import views.deliver
app.register_blueprint(views.deliver.bpDeliver, url_prefix = '/deliver')

import views.fin
app.register_blueprint(views.fin.bpFin, url_prefix = '/fin')


import views.customer
app.register_blueprint(views.customer.bpCustomer, url_prefix = '/customer')

import views.warehouse
app.register_blueprint(views.warehouse.bpWarehouse, url_prefix = '/warehouse')

import views.inventory
app.register_blueprint(views.inventory.bpInventory, url_prefix = '/inventory')

#===============================================================================
# import the customize filter and testing
#===============================================================================
import util.filters as filters
for f in filters.__all__ : app.jinja_env.filters[f] = getattr(filters, f)

import util.tests as tests
for t in tests.__all__ : app.jinja_env.tests[t] = getattr(tests, t)



#===============================================================================
# import the global vars into the template
#===============================================================================
import constant
for c in dir(constant) :
    if c.isupper() : app.jinja_env.globals[c] = getattr(constant, c)

