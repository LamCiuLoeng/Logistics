# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-13
#  @author: cl.lam
#  Description:
###########################################
'''
from flask.blueprints import Blueprint
from flask.views import View
from flask.helpers import url_for, flash
from werkzeug.utils import redirect

from sys2do.util.decorator import templated
from sys2do.views import BasicView
from sys2do.model import DBSession
from sys2do.model.auth import User
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION

__all__ = ['bpAdmin']

bpAdmin = Blueprint('bpAdmin', __name__)

class AdminView(BasicView):

    @templated('admin/index.html')
    def index(self):
        return {}

    @templated('admin/user_index.html')
    def users(self):
        users = DBSession.query(User).filter(User.active == 0).order_by(User.name).all()
        return {'records' : users}




bpAdmin.add_url_rule('/', view_func = AdminView.as_view('view'), defaults = {'action':'index'})
bpAdmin.add_url_rule('/<action>', view_func = AdminView.as_view('view'))
