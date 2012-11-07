# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
from sqlalchemy.sql.expression import and_, func
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
        result = DBSession.query(InventoryLocation).filter(InventoryLocation.active == 0).order_by(InventoryLocation.id)
        return {'result' : result}

    @templated('warehouse/add.html')
    def add(self):
        root_locations = DBSession.query(InventoryLocation).filter(and_(InventoryLocation.active == 0,
                                                       InventoryLocation.parent_id == None)).order_by(InventoryLocation.name)

        return {'locations' : root_locations}


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
                parent = DBSession.query(InventoryLocation).get(obj.parent_id)
                obj.full_path = "%s%s" % (parent.full_path or '', params['name'])
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
        root_locations = DBSession.query(InventoryLocation).filter(and_(InventoryLocation.active == 0,
                                                       InventoryLocation.parent_id == None)).order_by(InventoryLocation.name)
        return {'obj' : obj, 'locations' : root_locations}


    def save_update(self):
        id = _g('id')
#        try:
        obj = DBSession.query(InventoryLocation).get(id)
        for f in ["name", "manager", "address", "remark", ]: setattr(obj, f, _g(f))

        #if the parent_id change:
        old_parent_id = unicode(obj.parent_id) if obj.parent_id else None
        new_parent_id = _g('parent_id') or None

        if old_parent_id != new_parent_id:

            old_full_path = obj.full_path
            old_full_ids = "%s|" % obj.full_path_ids
            if new_parent_id:
                new_parent = DBSession.query(InventoryLocation).get(new_parent_id)
                new_full_path = new_parent.full_path + obj.name
                new_full_ids = "%s|%s|" % (new_parent.full_path_ids, obj.id)
            else:
                new_full_path = obj.name
                new_full_ids = "%s|" % obj.id
            sql1 = "update master_inventory_location set full_path = replace(full_path,'%s','%s') where full_path like '%s%%';"
            sql2 = "update master_inventory_location set full_path_ids = replace(full_path_ids,'%s','%s') where full_path_ids like '%s%%';"
            DBSession.execute(sql1 % (old_full_path, new_full_path, old_full_path))
            DBSession.execute(sql2 % (old_full_ids, new_full_ids, old_full_ids))

            obj.parent_id = new_parent_id
            obj.full_path = new_full_path
            obj.full_path_ids = new_full_ids[:-1]

        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
#        except:
#            DBSession.rollback()
#            _error(traceback.print_exc())
#            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
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
