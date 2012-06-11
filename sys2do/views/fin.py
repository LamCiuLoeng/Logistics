# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
from sys2do.views import BasicView
from flask.blueprints import Blueprint
from sys2do.util.decorator import templated, login_required
from sys2do.model.master import Warehouse
from sys2do.model import DBSession
from sys2do.util.common import _g
from flask.helpers import flash
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC
from werkzeug.utils import redirect



__all__ = ['bpFin']

bpFin = Blueprint('bpFin', __name__)

class FinView(BasicView):

    decorators = [login_required]

    @templated('warehouse/index.html')
    def index(self):
        pass

bpFin.add_url_rule('/', view_func = bpFin.as_view('view'), defaults = {'action':'index'})
bpFin.add_url_rule('/<action>', view_func = bpFin.as_view('view'))
