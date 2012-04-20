# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-6
#  @author: cl.lam
#  Description:
###########################################
'''
from flask.blueprints import Blueprint
from flask.views import View
from flask.helpers import url_for, flash
from sqlalchemy.sql.expression import and_
from werkzeug.utils import redirect

from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION, MESSAGE_INFO, \
    MSG_SAVE_SUCC, IN_STORE, OUT_STORE, MSG_UPDATE_SUCC, ORDER_NEW
from sys2do.util.decorator import templated
from sys2do.model import DBSession
from sys2do.views import BasicView
from sys2do.model.logic import DeliverHeader, OrderHeader, OrderDetail, \
    DeliverDetail, OrderLog
from sys2do.util.common import _gl, _g, _gp, getOr404
from sys2do.util.logic_helper import getDeliverNo, updateDeliverHeaderStatus
from sys2do.model.master import WarehouseItem


__all__ = ['bpDeliver']


bpDeliver = Blueprint('bpDeliver', __name__)

class DeliverView(BasicView):

    @templated('deliver/index.html')
    def index(self):
        result = DBSession.query(DeliverHeader).filter(DeliverHeader.active == 0)
        return {'result' : result}

    @templated('deliver/select_orders.html')
    def select_orders(self):
        result = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderHeader.status == IN_STORE[0])).all()
        return {'result' : result}



    @templated('deliver/add_deliver.html')
    def add_deliver(self):
        ids = _gl('order_ids')
        result = []
        for id in ids:
            header = DBSession.query(OrderHeader).get(id)
            result.append((header, [d for d in header.details if d.status == IN_STORE[0]]))

        return {'result' : result, }



    def deliver_save_new(self):

        header = DeliverHeader(no = getDeliverNo())
#        orders = []

        details = _gp('detail_')
        deliver_qtys = _gp('deliver_qty_')


        for (k, v), (dk, dv) in zip(details, deliver_qtys):
            n, id = k.split("_")
            deliver_qty = int(_g('deliver_qty_%s' % id))
            if deliver_qty > 0 :
                detail = DBSession.query(OrderDetail).get(id)
                DBSession.add(DeliverDetail(header = header, order_detail = detail, deliver_qty = deliver_qty))
                detail.future_warehouse_qty -= deliver_qty
#            detail.status = 1
#            if detail.header not in orders : orders.append(detail.header)

#        for order in orders:
#            if any(map(lambda d : d.status == IN_STORE, order.details)):
#                order.status = IN_STORE[0]
#            else:
#                order.status = OUT_STORE[0]

        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(self.default())

    @templated('deliver/view.html')
    def view(self):
        id = _g('id')
        h = DBSession.query(DeliverHeader).get(id)
        return {'header' : h}


    def update_status(self):
        header = getOr404(DeliverHeader, _g('id'))
        status = int(_g('sc'))
        (oheaders, odetails) = updateDeliverHeaderStatus(header.id, status)

        if status == OUT_STORE[0]: #remove the item from warehouse if it's out store action
            for d in header.details:
                record = DBSession.query(WarehouseItem).filter(WarehouseItem.order_detail_id == d.order_detail_id).one()
                record.qty -= d.deliver_qty
                if record.qty <= 0 : record.active = 1
                d.order_detail.warehouse_qty -= d.deliver_qty

        for oheader in oheaders:
            DBSession.add(OrderLog(order = oheader, remark = _g('remark')))


        DBSession.commit()
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect(self.default())


bpDeliver.add_url_rule('/', view_func = DeliverView.as_view('view'), defaults = {'action':'index'})
bpDeliver.add_url_rule('/<action>', view_func = DeliverView.as_view('view'))

