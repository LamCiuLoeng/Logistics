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
    MSG_SAVE_SUCC, IN_STORE, OUT_STORE, MSG_UPDATE_SUCC
from sys2do.util.decorator import templated
from sys2do.model import DBSession
from sys2do.views import BasicView
from sys2do.model.logic import DeliverHeader, OrderHeader, OrderDetail, \
    DeliverDetail, OrderLog
from sys2do.util.common import _gl, _g, _gp, getOr404
from sys2do.util.logic_helper import getDeliverNo
from sys2do.model.master import WarehouseItem


__all__ = ['bpDeliver']


bpDeliver = Blueprint('bpDeliver', __name__)

class DeliverView(BasicView):

    @templated('deliver/index.html')
    def index(self):
        result = DBSession.query(DeliverHeader).filter(DeliverHeader.active == 0)
        return {'result' : result}

    @templated('deliver/add.html')
    def add(self):
        result = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderDetail.status == 0 , OrderHeader.id == OrderDetail.header_id))
        return {'result' : result}

    @templated('deliver/add_deliver.html')
    def add_deliver(self):
        ids = _gl('order_ids')
        result = []
        for id in ids:
            header = DBSession.query(OrderHeader).get(id)
            result.append((header, [d for d in header.details if d.status == 0]))

        return {'result' : result, }



    def deliver_save_new(self):

        header = DeliverHeader(no = getDeliverNo())
        orders = []
        for k, v in _gp('detail_'):
            n, id = k.split("_")
            detail = DBSession.query(OrderDetail).get(id)
            DBSession.add(DeliverDetail(header = header, order_detail = detail))
            detail.status = 1
            if detail.header not in orders : orders.append(detail.header)

        for order in orders:
            if any(map(lambda d : d.status == IN_STORE, order.details)):
                order.status = IN_STORE[0]
            else:
                order.status = OUT_STORE[0]

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
        header.status = status

        for d in header.details:
            d.order_detail.status = status
            if status == OUT_STORE[0]:
                record = DBSession.query(WarehouseItem).filter(WarehouseItem.order_detail_id == d.order_detail_id).one()
                record.active = 1


        for order in header.get_related_orders():
            if all(map(lambda d : d.status == status, order.details)):
                order.status = status
                DBSession.add(OrderLog(order = order, remark = _g('remark')))



        DBSession.commit()
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect(self.default())


bpDeliver.add_url_rule('/', view_func = DeliverView.as_view('view'), defaults = {'action':'index'})
bpDeliver.add_url_rule('/<action>', view_func = DeliverView.as_view('view'))

