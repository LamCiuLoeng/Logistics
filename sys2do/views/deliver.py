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
    MSG_SAVE_SUCC, IN_WAREHOUSE, MSG_UPDATE_SUCC, ORDER_NEW, \
    ORDER_CANCELLED, MSG_DELETE_SUCC, SORTING, MSG_RECORD_NOT_EXIST, SEND_OUT, \
    GOODS_ARRIVED, IN_TRAVEL, GOODS_SIGNED
from sys2do.util.decorator import templated
from sys2do.model import DBSession
from sys2do.views import BasicView
from sys2do.model.logic import DeliverHeader, OrderHeader, OrderDetail, \
    DeliverDetail, OrderLog, DeliverLog
from sys2do.util.common import _gl, _g, _gp, getOr404, getMasterAll, _debug
#from sys2do.util.logic_helper import updateDeliverHeaderStatus
from sys2do.model.master import WarehouseItem, Supplier


__all__ = ['bpDeliver']


bpDeliver = Blueprint('bpDeliver', __name__)

class DeliverView(BasicView):

    @templated('deliver/index.html')
    def index(self):
        result = DBSession.query(DeliverHeader).filter(DeliverHeader.active == 0)
        return {'result' : result}

    @templated('deliver/select_orders.html')
    def select_orders(self):
        result = DBSession.query(OrderDetail).filter(and_(OrderDetail.active == 0, OrderDetail.status < SORTING[0])).all()
        return {'result' : result}



    @templated('deliver/add_deliver.html')
    def add_deliver(self):
        ids = _gl('order_detail_ids')
        order_details = DBSession.query(OrderDetail).filter(OrderDetail.id.in_(ids))
        suppliers = getMasterAll(Supplier)
        return {'result' : order_details, 'suppliers' : suppliers}


    def deliver_save_new(self):

        header = DeliverHeader(no = _g('no'),
                               destination_address = _g('destination_address'),
                               supplier_id = _g('supplier_id'),
                               supplier_contact = _g('supplier_contact'),
                               supplier_tel = _g('supplier_tel'),
                               expect_time = _g('expect_time'),
                               remark = _g('remark'),
                               )

        line_no = 1
        for k, id in _gp('detail_'):
            order_detail = DBSession.query(OrderDetail).get(id)
            DBSession.add(DeliverDetail(header = header,
                                        order_detail = order_detail,
                                        order_detail_line_no = order_detail.line_no,
                                        line_no = line_no))
            order_detail.status = SORTING[0]
            line_no += 1
            _debug('------- save detail')
        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(self.default())

    @templated('deliver/view.html')
    def view(self):
        id = _g('id')
        h = DBSession.query(DeliverHeader).get(id)
        return {'header' : h, 'values' : h.populate() , 'details' : h.details}


    @templated('deliver/revise_deliver.html')
    def revise(self):
        header = getOr404(DeliverHeader, _g('id'), redirect_url = self.default())
        return {'values' : header.populate(), 'details' : header.details, 'suppliers' : getMasterAll(Supplier)}


    def deliver_save_revise(self):
        pass

    def delete(self):
        header = getOr404(DeliverHeader, _g('id'), redirect_url = self.default())
        header.status = ORDER_CANCELLED[0]
        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))


    def do_action(self):
        header = DeliverHeader.get(_g('id'))
        if not header :
            flash(MSG_RECORD_NOT_EXIST)
            return redirect(self.default())

        if _g('sc') not in ['SEND_OUT', 'GOODS_ARRIVED']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(self.default())

        if _g('sc') == 'SEND_OUT' :
            header.send_out_remark = _g('send_out_remark')
            header.status = SEND_OUT[0]
            for d in header.details :
                d.status = SEND_OUT[0]
                d.order_detail.status = SEND_OUT[0]
        elif _g('sc') == 'GOODS_ARRIVED':
            header.actual_time = _g('actual_time')
            header.  arrived_remark = _g('arrived_remark')
            header.status = GOODS_ARRIVED[0]
            for d in header.details :
                d.status = GOODS_ARRIVED[0]
                d.order_detail.status = GOODS_ARRIVED[0]
                d.order_detail.actual_time = _g('actual_time')

        DBSession.commit()
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect(self.default())



    def update_status(self):
        header = getOr404(DeliverHeader, _g('id'))
        status = int(_g('sc'))
        (oheaders, odetails) = updateDeliverHeaderStatus(header.id, status)

        if status == OUT_WAREHOUSE[0]: #remove the item from warehouse if it's out store action
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


    @templated('deliver/vendor_select.html')
    def vendor_select(self):
        result = DBSession.query(DeliverHeader).filter(and_(DeliverHeader.active == 0, DeliverHeader.status.in_([SEND_OUT[0], IN_TRAVEL[0]]))).order_by(DeliverHeader.create_time)
        return {'result' : result , 'values' : {
                                                'no' : _g('no'),
                                                'destination_address' : _g('destination_address'),
                                                'create_time_from' : _g('create_time_from'),
                                                'create_time_to' : _g('create_time_to'),
                                                }}

    @templated('deliver/vendor_input.html')
    def vendor_input(self):
        header = DeliverHeader.get(_g('id'))
        if not header :
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))

        return {'values' : header.populate(), 'details' : header.details }


    def vendor_input_save(self):
        header = DeliverHeader.get(_g('id'))
        if not header :
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))


        if _g('type') == "IN_TRAVEL" : new_status = IN_TRAVEL[0]
        elif _g('type') == "GOODS_ARRIVED" : new_status = GOODS_ARRIVED[0]
        elif _g('type') == "GOODS_SIGNED" : new_status = GOODS_SIGNED[0]
        else:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))

        for d in header.details:
            d.status = new_status
            d.order_detail.status = new_status

        log = DeliverLog(deliver_header_id = header.id, remark = _g('remark'))

        DBSession.add(log)
        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'vendor_select'))

bpDeliver.add_url_rule('/', view_func = DeliverView.as_view('view'), defaults = {'action':'index'})
bpDeliver.add_url_rule('/<action>', view_func = DeliverView.as_view('view'))

