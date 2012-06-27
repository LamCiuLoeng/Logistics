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
import traceback

from flask import Blueprint, render_template, url_for, session, Response
from flask.views import View
from werkzeug.utils import redirect
from flask.helpers import flash, jsonify

from sys2do.model.logic import OrderHeader, TransferLog, \
    DeliverDetail
from sys2do.model import DBSession
from sys2do.util.decorator import templated, login_required
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, STATUS_LIST, IN_TRAVEL, \
    MSG_RECORD_NOT_EXIST, ASSIGN_PICKER, IN_WAREHOUSE, ASSIGN_PICKER, \
    LOG_CREATE_ORDER, LOG_SEND_PICKER, LOG_GOODS_IN_WAREHOUSE, ORDER_NEW
from sys2do.views import BasicView
from sys2do.util.common import _g, getOr404, _gp, getMasterAll, _debug, _info
from sys2do.model.master import CustomerProfile, InventoryLocation, \
    Customer, ItemUnit, WeightUnit, ShipmentType, \
    InventoryItem, Payment, Ratio
from sys2do.util.logic_helper import genSystemNo
from sqlalchemy.sql.expression import and_
from sys2do.util.barcode_helper import generate_barcode_file
from flask.globals import request


__all__ = ['bpOrder']

bpOrder = Blueprint('bpOrder', __name__)

class OrderView(BasicView):

#    decorators = [login_required]

    @templated('order/index.html')
#    @login_required
    def index(self):
        result = DBSession.query(OrderHeader).filter(OrderHeader.active == 0)
        return {'result' : result }


    @templated('order/add.html')
    def add(self):
        ratios = {}
        for r in DBSession.query(Ratio).filter(Ratio.active == 0):
            ratios[r.type] = r.value
        return {'customers' :getMasterAll(Customer),
#                'units' : getMasterAll(ItemUnit),
#                'wunits' : getMasterAll(WeightUnit),
#                'shiptype' : getMasterAll(ShipmentType),
                'payment' : getMasterAll(Payment),
                'ratios' : ratios,
                }


    def save_new(self):
        code = self._save_new_process()
        if code == 0:
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        else:
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view', action = 'index'))



    def _save_new_process(self):
        params = {}
        for k in ['source_station', 'source_company', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                  'destination_station', 'destination_company', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                  'no', 'order_time', 'item', 'expect_time', 'remark',
                 'payment_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
                  'weight', 'weight_ratio', 'weight_ratio', 'amount',
                  ]:
            params[k] = _g(k)
        order = OrderHeader(**params)
        DBSession.add(order)
        order.barcode = generate_barcode_file(order.no)
        DBSession.add(TransferLog(
                                  refer_id = order.id,
                                  transfer_date = dt.now().strftime("%Y-%m-%d"),
                                  type = 0,
                                  remark = unicode(LOG_CREATE_ORDER),
                                  ))
        DBSession.commit()
        return 0




    @templated('order/review.html')
    def review(self):
        header = getOr404(OrderHeader, _g('id'))
        if header.status in [ASSIGN_PICKER[0], ]:
            locations = DBSession.query(InventoryLocation).filter(InventoryLocation.active == 0).order_by(InventoryLocation.full_path)
        else:
            locations = []
        return {'header' : header , 'details' : header.details, 'locations' : locations}


    @templated('order/revise.html')
    def revise(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)
        return {
                'header' : header ,
                'payment' : getMasterAll(Payment),
                }


    def save_update(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)
        try:
            for k in ['source_station', 'source_company', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                  'destination_station', 'destination_company', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                  'no', 'order_time', 'item', 'expect_time', 'remark',
                 'payment_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
                  'weight', 'weight_ratio', 'weight_ratio', 'amount',
                  ]:
                setattr(header, k, _g(k) or None)

            DBSession.commit()
        except:
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            DBSession.rollback()
        else:
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'index'))



    def delete(self):
        header = getOr404(OrderHeader, _g('id'), redirect_url = self.default())
        header.status = ORDER_CANCELLED[0]
        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))


    def do_action(self):
        header = OrderHeader.get(_g('id'))

        if not header :
            flash(MSG_RECORD_NOT_EXIST)
            return redirect(self.default())

        if _g('sc') == 'ASSIGN_PICKER' :
            header.receiver = _g('receiver')
            header.receiver_contact = _g('receiver_contact')
            header.receiver_remark = _g('receiver_remark')
            header.status = ASSIGN_PICKER[0]
            for d in header.details: d.status = ASSIGN_PICKER[0]

            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = dt.now().strftime("%Y-%m-%d"),
                                      type = 0,
                                      remark = LOG_SEND_PICKER
                                      ))

        elif _g('sc') == 'IN_WAREHOUSE' :
            header.in_warehouse_remark = _g('in_warehouse_remark')
            header.status = IN_WAREHOUSE[0]
            location_id = _g('location_id')
            for d in header.details:
                d.status = IN_WAREHOUSE[0]

                if location_id:
                    DBSession.add(InventoryItem(
                                                item = d.item,
                                                location_id = location_id,
                                                qty = d.order_qty,
                                                refer_order_header = unicode(header),
                                                refer_order_detail_id = d.id,
                                                ))

            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = dt.now().strftime("%Y-%m-%d"),
                                      type = 0,
                                      remark = LOG_GOODS_IN_WAREHOUSE
                                      ))

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










    #===========================================================================
    # not very important
    #===========================================================================
    @templated('order/add_by_customer.html')
    def add_by_customer(self):

        if not session.get('customer_profile', None) or not session['customer_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))
        return {
                'units' : getMasterAll(ItemUnit),
                'wunits' : getMasterAll(WeightUnit),
                'shiptype' : getMasterAll(ShipmentType),
                }


    #===========================================================================
    # not very important
    #===========================================================================
    def save_new_by_customer(self):
        code = self._save_new_process()
        if code == 0:
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        else:
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view', action = 'search_by_customer'))


    @templated('order/search_by_customer.html')
    def search_by_customer(self):
        if not session.get('customer_profile', None) or not session['customer_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))
        conditions = [OrderHeader.active == 0,
                      OrderDetail.active == 0,
                      OrderHeader.id == OrderDetail.header_id,
                      OrderHeader.customer_id == session['customer_profile']['id'],
                      ]
        if _g('no'):
            conditions.append(OrderHeader.no.like('%%%s%%' % _g('no')))
        if _g('destination_address'):
            conditions.append(OrderDetail.destination_address.like(_g('destination_address')))
        if _g('create_time_from'):
            conditions.append(OrderHeader.create_time > _g('create_time_from'))
        if _g('create_time_to'):
            conditions.append(OrderHeader.create_time < _g('create_time_to'))

        result = DBSession.query(OrderHeader, OrderDetail).filter(and_(*conditions)).order_by(OrderHeader.no)
        return {'result' : result, 'values' : {
                                              'no' : _g('no'), 'destination_address' : _g('destination_address'),
                                              'create_time_from' : _g('create_time_from'), 'create_time_to' : _g('create_time_to')
                                              }}



    @templated('order/search_transfer_log.html')
    def search_transfer_log(self):
        header = OrderHeader.get(_g('id'))

        if not header :
            flash(MSG_RECORD_NOT_EXIST)
            return redirect(self.default())

        order_log = header.get_logs()
        detail_log = {}
        for d in header.details:
            logs = []
            for dd in DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == d.id)).order_by(DeliverDetail.id):
                logs.extend(dd.header.get_logs())
            detail_log[d.id] = logs

        return {'order_log' : order_log, 'detail_log' : detail_log}


    def ajax_todo_list(self):
        new_orders = DBSession.query(OrderHeader).filer(and_(OrderHeader.active == 0 , OrderHeader.status == ORDER_NEW[0])).order_by(OrderHeader.create_time).all()
        return jsonify(result = 0, data = [{'id' : order.id, 'no' : unicode(order)} for order in new_orders])


    @templated('order/barcode.html')
    def barcode(self):
        header = OrderHeader.get(_g('id'))

        if not header :
            flash(MSG_RECORD_NOT_EXIST)
            return redirect(self.default())

        return {'header' : header}


    def hh(self):
        print request.values
        type = _g('type')
        barcode = _g('barcode')

        if type == 'search':
            try:
                d = DBSession.query(OrderDetail).filter(OrderDetail.no == barcode).one()
                h = d.header
                params = {
                          'NO' : h.no,
                          'CUSTOMER' : unicode(h.customer),
                          'TEL' : h.source_tel,
                          'DESTINATION' : d.destination_full_address,
                          }
            except:
                params = {
                          'NO' : 'NO SUCH NO#',
                          'CUSTOMER' : '',
                          'TEL' : '',
                          'DESTINATION' : '',
                          }

            xml = []
            xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
            xml.append('<ORDER>')
            xml.append('<NO>%s</NO>' % params['NO'])
            xml.append('<CUSTOMER>%s</CUSTOMER>' % params['CUSTOMER'])
            xml.append('<TEL>%s</TEL>' % params['TEL'])
            xml.append('<DESTINATION>%s</DESTINATION>' % params['DESTINATION'])
            xml.append('</ORDER>')
            rv = app.make_response("".join(xml))
            rv.mimetype = 'text/xml'
            return rv
        elif type == 'submit':
            try:
                d = DBSession.query(OrderDetail).filter(OrderDetail.no == barcode).one()
                d.update_status(_g('id'))
                DBSession.commit()
                return unicode(MSG_UPDATE_SUCC)
            except:
                return unicode(MSG_RECORD_NOT_EXIST)
        else:
            return unicode(MSG_NO_SUCH_ACTION)



bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

