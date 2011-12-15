# -*- coding: utf-8 -*-
from flask.views import View
from flask.helpers import url_for, flash
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION
from werkzeug.utils import redirect

__all__ = ['BasicView']



class BasicView(View):
    methods = ['GET', 'POST']
#    decorators = [login_required]

    def default(self):  return url_for('.view', action = 'index')

    def dispatch_request(self, action):
        try:
            return getattr(self, action)()
        except AttributeError, e:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(self.default())
