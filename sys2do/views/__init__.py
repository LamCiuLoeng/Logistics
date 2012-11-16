# -*- coding: utf-8 -*-
from flask import g
from flask.views import View
from flask.helpers import url_for, flash
from werkzeug.utils import redirect
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION
from sys2do import app
from sys2do.model import DBSession


__all__ = ['BasicView']



class BasicView(View):
    methods = ['GET', 'POST']
#    decorators = [login_required]

    def default(self):  return url_for('.view', action = 'index')

    def dispatch_request(self, action):
#        try:
#            return getattr(self, action)()
#        except AttributeError, e:
#            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
#            return redirect(self.default())

        return getattr(self, action)()


@app.before_request
def before_request():  # occur before the request
    DBSession()


@app.teardown_request
def teardown_request(param):  # if error occur on the controller
    DBSession.remove()  # to cleare the nested rollback


@app.after_request
def after_request(response):
    return response
