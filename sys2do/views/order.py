# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-28
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
from datetime import timedelta

from flask import Blueprint

from flask.views import View
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from sys2do.model.logic import OrderHeader, OrderLog, OrderDetail
from sys2do.model import DBSession
from sys2do.util.decorator import templated, login_required
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, RECEIVED_GOODS, STATUS_LIST, IN_TRAVEL, \
    IN_STORE
from sys2do.views import BasicView
from sys2do.util.common import _g, getOr404, _gp
from sys2do.model.master import CustomerProfile, WarehouseItem, Warehouse
from sys2do.util.logic_helper import genSystemNo
from sqlalchemy.sql.expression import and_


__all__ = ['bpOrder']

bpOrder = Blueprint('bpOrder', __name__)

class OrderView(BasicView):

    @templated('order/index.html')
    def index(self):
        result = DBSession.query(OrderHeader).filter(OrderHeader.active == 0)
        return {'result' : result }

    @templated('order/add.html')
    def add(self):
        cps = DBSession.query(CustomerProfile).all()
        companys = []
        vendors = []
        items = []
        for cp in cps:
            companys.extend(cp.customers)
            vendors.extend(cp.vendors)
            items.extend(cp.items)
        return {'companys' :companys , 'vendors' : vendors, 'items' : items}


    def save_new(self):
        c = _g('company')
        v = _g('vendor')

        no = genSystemNo()
        order = OrderHeader(no = no, customer_id = c, vendor_id = v)
        DBSession.add(order)

        for k, v in _gp('item_'):
            n, id = k.split("_")
            DBSession.add(OrderDetail(header = order, item_id = id, qty = v))

        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))



    @templated('order/revise.html')
    def revise(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)
        values = header.populate()

        ws = DBSession.query(Warehouse).filter(Warehouse.active == 0).order_by(Warehouse.name)

        return {'values' : values , 'details' : header.details , 'warehouses' : ws}


    def save_update(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)

        fields = ['no', 'customer', ]
        try:
            for f in fields:
                setattr(header, f, _g(f) or None)

            DBSession.commit()
        except:
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            DBSession.rollback()
        else:
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'index'))



    def cancel(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)
        header.status = ORDER_CANCELLED[0]
        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))


    def do_action(self):
        header = getOr404(OrderHeader, _g('id'), self.default())
        status = int(_g('sc'))

        #update the order and detail's status
        header.update_status(status)

        DBSession.add(OrderLog(order_id = _g('id'), remark = _g('remark')))

        #if it's in store, update the warehouse items qty
        if status == IN_STORE[0]:
            for d in header.details:
                DBSession.add(WarehouseItem(item_id = d.item_id, warehouse_id = _g('warehouse_id'), qty = d.order_qty, order_detail_id = d.id))
                d.warehouse_qty = d.future_warehouse_qty = d.order_qty #make the warehouse qty

        DBSession.commit()
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect(self.default())

    @templated('order/warning.html')
    def warning(self):
        t = _g('t') or None
        if not t : return {'result' : [] , 't' : t}

        n = dt.now() + timedelta(int(t))
        result = DBSession.query(OrderHeader).filter(and_(OrderHeader.status == IN_TRAVEL[0], OrderHeader.expect_time > n)).order_by(OrderHeader.expect_time)
        return {'result' : result, 't' : t}


bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

