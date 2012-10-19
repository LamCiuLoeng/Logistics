# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
from sqlalchemy.sql.expression import and_
import traceback
from werkzeug.utils import redirect
from flask.blueprints import Blueprint
from flask.helpers import flash


from sys2do.views import BasicView
from sys2do.util.decorator import templated, login_required
from sys2do.model.master import InventoryLocation, InventoryItem
from sys2do.model import DBSession
from sys2do.util.common import _g, _error
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC, MSG_SERVER_ERROR, \
    MESSAGE_ERROR




__all__ = ['bpWarehouse']

bpWarehouse = Blueprint('bpWarehouse', __name__)

class WarehouseView(BasicView):

#    decorators = [login_required]

    @templated('warehouse/index.html')
    def index(self):
        result = DBSession.query(InventoryLocation).filter(InventoryLocation.active == 0).order_by(InventoryLocation.full_path)
        return {'result' : result}

    @templated('warehouse/add.html')
    def add(self):
        locations = DBSession.query(InventoryLocation).filter(InventoryLocation.active == 0).order_by(InventoryLocation.full_path)
        return {'locations' : locations}


    def save_new(self):
        params = {
                   "name" : _g('name'),
                   "address" : _g('address'),
                   "manager" : _g('manager'),
                   "remark" : _g('remark'),
                   "parent_id" : _g('parent_id'),
                  }

        try:
            obj = InventoryLocation(**params)
            DBSession.add(obj)
            DBSession.flush()

            if params['parent_id']:
                parent = DBSession.query(InventoryLocation).get(params['parent_id'])
                obj.full_path = "%s%s" % (parent.full_path, params['name'])
                obj.full_path_ids = "%s|%s" % (parent.full_path_ids, obj.id)
            else:
                obj.full_path = params['name']
                obj.full_path_ids = obj.id

            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
        return redirect(self.default())


    @templated("warehouse/update.html")
    def update(self):
        id = _g('id')
        obj = DBSession.query(InventoryLocation).get(id)
        locations = DBSession.query(InventoryLocation).filter(InventoryLocation.active == 0).order_by(InventoryLocation.full_path)
        return {'obj' : obj, 'locations' : locations}


    def save_update(self):
        id = _g('id')
        try:
            obj = DBSession.query(InventoryLocation).get(id)
            for f in ["name", "manager", "address", "remark", "parent_id"]:
                setattr(obj, f, _g(f))

            parent_id = _g('parent_id')
            if parent_id:
                parent = DBSession.query(InventoryLocation).get(parent_id)
                obj.full_path = "".join([parent.full_path, obj.name])
                obj.full_path_ids = "%s|%s" % (parent.full_path_ids, obj.id)
            else:
                obj.full_path = obj.name
                obj.full_path_ids = obj.id


            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(self.default())



    @templated('warehouse/view_items.html')
    def view_items(self):
        id = _g('id')
        w = DBSession.query(InventoryLocation).get(id)
        ids = w.full_path_ids.split("|")

        result = DBSession.query(InventoryItem, InventoryLocation).filter(and_(
                                                   InventoryItem.active == 0,
                                                   InventoryItem.location_id.in_(ids),
                                                   InventoryLocation.active == 0,
                                                   InventoryItem.location_id == InventoryLocation,
                                                   )).order_by(InventoryItem.create_time).all()
        return {'result' : result , 'location' : w}


bpWarehouse.add_url_rule('/', view_func = WarehouseView.as_view('view'), defaults = {'action':'index'})
bpWarehouse.add_url_rule('/<action>', view_func = WarehouseView.as_view('view'))
