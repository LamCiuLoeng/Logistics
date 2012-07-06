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
    DeliverDetail, ItemDetail, PickupDetail
from sys2do.model import DBSession
from sys2do.util.decorator import templated, login_required
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, STATUS_LIST, IN_TRAVEL, \
    MSG_RECORD_NOT_EXIST, IN_WAREHOUSE, \
    LOG_CREATE_ORDER, LOG_GOODS_IN_WAREHOUSE, ORDER_NEW, \
    ASSIGN_RECEIVER, LOG_SEND_RECEIVER
from sys2do.views import BasicView
from sys2do.util.common import _g, getOr404, _gp, getMasterAll, _debug, _info, \
    _gl
from sys2do.model.master import CustomerProfile, InventoryLocation, \
    Customer, ItemUnit, WeightUnit, ShipmentType, \
    InventoryItem, Payment, Ratio, PickupType, PackType
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
        values = {}
        for f in ['create_time_from', 'create_time_to', 'no', 'source_station', 'source_company', 'destination_station', 'destination_company'] :
            values[f] = _g(f)

        conditions = [OrderHeader.active == 0]
        if values['create_time_from']:
            conditions.append(OrderHeader.create_time > values['create_time_from'])
        if values['create_time_to']:
            conditions.append(OrderHeader.create_time < values['create_time_to'])
        if values['no']:
            conditions.append(OrderHeader.no.op('like')('%%%s%%' % values['no']))
        if values['source_station']:
            conditions.append(OrderHeader.source_station.op('like')('%%%s%%' % values['source_station']))
        if values['source_company']:
            conditions.append(OrderHeader.source_company.op('like')('%%%s%%' % values['source_company']))
        if values['destination_station']:
            conditions.append(OrderHeader.destination_station.op('like')('%%%s%%' % values['destination_station']))
        if values['destination_company']:
            conditions.append(OrderHeader.destination_company.op('like')('%%%s%%' % values['destination_company']))

        result = DBSession.query(OrderHeader).filter(and_(*conditions))
        return {'result' : result , 'values' : values}


    @templated('order/add.html')
    def add(self):
        ratios = {}
        for r in DBSession.query(Ratio).filter(Ratio.active == 0):
            ratios[r.type] = r.value
        return {'customers' :getMasterAll(Customer),
#                'units' : getMasterAll(ItemUnit),
#                'wunits' : getMasterAll(WeightUnit),
#                'shiptype' : getMasterAll(ShipmentType),
                'payment' : getMasterAll(Payment, 'id'),
                'pickup_type' : getMasterAll(PickupType, 'id'),
                'pack_type' : getMasterAll(PackType, 'id'),
                'ratios' : ratios,
                'current' : dt.now().strftime("%Y-%m-%d %H:%M")
                }


    def save_new(self):
        try:
            code, header = self._save_new_process()
            if code == 0:
                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            else:
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)

            for nk, nv in _gp('item_name_'):
                id = nk.split("_")[2]
                DBSession.add(ItemDetail(
                                         header = header, item = nv , qty = _g("item_qty_%s" % id) ,
                                         vol = _g("item_vol_%s" % id), weight = _g("item_weight_%s" % id)
                                         ))
            DBSession.commit()
        except:
            DBSession.rollback()

        return redirect(url_for('.view', action = 'index'))




    def _save_new_process(self):
        params = {}
        for k in ['source_station', 'source_company', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                  'destination_station', 'destination_company', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                  'no', 'order_time', 'item', 'item_remark', 'expect_time', 'remark',
                 'payment_id', 'pickup_type_id', 'pack_type_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
                  'weight', 'weight_ratio', 'weight_ratio', 'amount',
                  ]:
            params[k] = _g(k)
        order = OrderHeader(**params)
        DBSession.add(order)
        order.barcode = generate_barcode_file(order.no)

        _info(type(order.no))

        DBSession.flush()
        DBSession.add(TransferLog(
                                  refer_id = order.id,
                                  transfer_date = dt.now().strftime("%Y-%m-%d"),
                                  type = 0,
                                  remark = unicode(LOG_CREATE_ORDER),
                                  ))
        return (0, order)

#
#
#
#    @templated('order/review.html')
#    def review(self):
#        header = getOr404(OrderHeader, _g('id'))
#        if header.status in [ASSIGN_PICKER[0], ]:
#            locations = DBSession.query(InventoryLocation).filter(InventoryLocation.active == 0).order_by(InventoryLocation.full_path)
#        else:
#            locations = []
#        return {'header' : header , 'details' : header.details, 'locations' : locations}


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
                'pickup_type' : getMasterAll(PickupType, 'id'),
                'pack_type' : getMasterAll(PackType, 'id'),
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


#
#    @templated('order/warning.html')
#    def warning(self):
#        t = _g('t') or None
#        if not t : return {'result' : [] , 't' : t}
#
#        n = dt.now() + timedelta(int(t))
#        result = DBSession.query(OrderHeader).filter(and_(OrderHeader.status == IN_TRAVEL[0], OrderHeader.expect_time > n)).order_by(OrderHeader.expect_time)
#        return {'result' : result, 't' : t}
#
#







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



    def ajax_save(self):
        type = _g('form_type')
        id = _g("id")
        if type not in ['order_header', 'item_detail', 'receiver' , 'transit', 'pickup']:
            return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})

        header = DBSession.query(OrderHeader).get(id)

        if type == 'order_header':
            fields = ['no', 'source_station', 'source_company', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                      'payment_id', 'item', 'qty', 'weight', 'vol', 'shipment_type_id',
                      'destination_station', 'destination_company', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                      'order_time', 'expect_time', 'actual_time', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'amount', 'cost', 'remark',
                      'pickup_type_id', 'pack_type_id',
                      ]
            for f in fields:
                setattr(header, f, _g(f))
            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})

        elif type == 'item_detail':
            action_type = _g('action_type')
            if action_type not in ['ADD', 'DELETE']: return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action_type == 'ADD' :
                params = {'header' : header}
                for f in ['item', 'qty', 'vol', 'weight', 'remark', ]:
                    params[f] = _g(f)
                obj = ItemDetail(**params)
                DBSession.add(obj)
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC) , 'id' : obj.id})
            else:
                line = DBSession.query(ItemDetail).get(_g('item_id'))
                line.active = 1
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})

        elif type == 'receiver' :
            for f in ['receiver_contact', 'receiver_tel', 'receiver_mobile', 'receiver_remark', ]:
                setattr(header, f, _g(f))

            if header.status < ASSIGN_RECEIVER[0]:
                header.update_status(ASSIGN_RECEIVER[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = dt.now().strftime("%Y-%m-%d"),
                                  type = 0,
                                  remark = unicode(LOG_SEND_RECEIVER),
                                  ))

            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})

        elif type == 'transit':
            action_type = _g('action_type')
            if action_type not in ['ADD', 'DELETE'] : return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action_type == 'ADD':
                obj = TransferLog(
                                  refer_id = header.id,
                                  transfer_date = _g('action_time'),
                                  type = 0,
                                  remark = _g('remark'),
                                  )
                DBSession.add(obj)
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC) , 'transit_id' : obj.id})
            else:
                transit_id = _g('transit_id')
                obj = DBSession.query(TransferLog).get(transit_id)
                obj.active = 1
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})

        elif type == 'pickup':
            action_type = _g('action_type')
            if action_type not in ['ADD', 'DELETE'] : return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action_type == 'ADD' :
                params = {}
                for f in ['action_time', 'contact', 'tel', 'qty', 'remark']: params[f] = _g(f)
                obj = PickupDetail(header = header, **params)
                DBSession.add(obj)
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC) , 'pickup_id' : obj.id})
            else:
                pickup_id = _g('pickup_id')
                obj = DBSession.query(PickupDetail).get(pickup_id)
                obj.active = 1
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})


bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

