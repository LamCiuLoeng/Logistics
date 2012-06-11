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



__all__ = ['bpWarehouse']

bpWarehouse = Blueprint('bpWarehouse', __name__)

class WarehouseView(BasicView):

    decorators = [login_required]

    @templated('warehouse/index.html')
    def index(self):
        result = DBSession.query(Warehouse).filter(Warehouse.active == 0)
        return {'result' : result}

    @templated('warehouse/add.html')
    def add(self):
        return {}

    def save_new(self):
        DBSession.add(Warehouse(name = _g('name'), address = _g('address'), manager = _g('manager'), remark = _g('remark')))
        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(self.default())

    @templated('warehouse/view_items.html')
    def view_items(self):
        id = _g('id')
        w = DBSession.query(Warehouse).get(id)
        return {'result' : w.items , 'warehouse' : w}

bpWarehouse.add_url_rule('/', view_func = WarehouseView.as_view('view'), defaults = {'action':'index'})
bpWarehouse.add_url_rule('/<action>', view_func = WarehouseView.as_view('view'))
