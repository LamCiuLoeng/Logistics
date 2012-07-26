# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-28
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt, timedelta
import os
import random
import shutil
import traceback

from webhelpers import paginate
from werkzeug.utils import redirect
from flask import Blueprint, render_template, url_for, session, Response
from flask.globals import request
from flask.helpers import flash, jsonify, send_file
from flask.views import View
from sqlalchemy.sql.expression import and_, desc
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, STATUS_LIST, IN_TRAVEL, MSG_RECORD_NOT_EXIST, \
    IN_WAREHOUSE, LOG_CREATE_ORDER, LOG_GOODS_IN_WAREHOUSE, ORDER_NEW, \
    ASSIGN_RECEIVER, LOG_SEND_RECEIVER, OUT_WAREHOUSE, GOODS_PICKUP, GOODS_SIGNED, \
    LOG_GOODS_SIGNED, LOG_GOODS_PICKUPED, LOG_GOODS_IN_TRAVEL, SORTING, \
    SYSTEM_DATETIME_FORMAT
from sys2do.model import DBSession
from sys2do.model.logic import OrderHeader, TransferLog, DeliverDetail, \
    ItemDetail, PickupDetail
from sys2do.model.master import CustomerProfile, InventoryLocation, Customer, \
    ItemUnit, WeightUnit, ShipmentType, InventoryItem, Payment, Ratio, PickupType, \
    PackType, CustomerTarget, Receiver, Item, Note, City, Province
from sys2do.setting import TMP_FOLDER, TEMPLATE_FOLDER, PAGINATE_PER_PAGE
from sys2do.util.barcode_helper import generate_barcode_file
from sys2do.util.common import _g, getOr404, _gp, getMasterAll, _debug, _info, \
    _gl, _error
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.util.excel_helper import SummaryReport
from sys2do.util.logic_helper import genSystemNo
from sys2do.views import BasicView



__all__ = ['bpOrder']

bpOrder = Blueprint('bpOrder', __name__)

class OrderView(BasicView):

    decorators = [login_required, tab_highlight('TAB_MAIN'), ]

    @templated('order/index.html')
#    @login_required
    def index(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['no', 'create_time_from', 'create_time_to', 'ref_no',
                      'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                      'source_company_id', 'destination_company_id',
                      'approve', 'paid', 'is_exception', 'is_less_qty'] :
                values[f] = _g(f)
            values['field'] = _g('field', None) or 'create_time'
            values['direction'] = _g('direction', None) or 'desc'

        else: #come from paginate or return
            values = session.get('order_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1

        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['order_values'] = values

        conditions = [OrderHeader.active == 0]
        if values.get('create_time_from', None):
            conditions.append(OrderHeader.create_time > values['create_time_from'])
        if values.get('create_time_to', None):
            conditions.append(OrderHeader.create_time < '%s 23:59' % values['create_time_to'])
        if values.get('ref_no', None):
            conditions.append(OrderHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values.get('no', None):
            conditions.append(OrderHeader.no.op('like')('%%%s%%' % values['no']))
        if values.get('source_province_id', None):
            conditions.append(OrderHeader.source_province_id == values['source_province_id'])
            sp = DBSession.query(Province).get(values['source_province_id'])
            source_cites = sp.children()
        else: source_cites = []
        if values.get('source_city_id', None):
            conditions.append(OrderHeader.source_city_id == values['source_city_id'])
        if values.get('destination_province_id', None):
            conditions.append(OrderHeader.destination_province_id == values['destination_province_id'])
            dp = DBSession.query(Province).get(values['destination_province_id'])
            destination_cites = dp.children()
        else: destination_cites = []
        if values.get('destination_city_id', None):
            conditions.append(OrderHeader.destination_city_id == values['destination_city_id'])

        if values.get('source_company_id', None):
            conditions.append(OrderHeader.source_company_id == values['source_company_id'])
            targets = DBSession.query(CustomerTarget).filter(and_(CustomerTarget.active == 0, CustomerTarget.customer_id == values['source_company_id']))
        else:
            targets = []

        if values.get('destination_company_id', None):
            conditions.append(OrderHeader.destination_company_id == values['destination_company_id'])
        if values.get('approve', None):
            conditions.append(OrderHeader.approve == values['approve'])
        if values.get('paid', None):
            conditions.append(OrderHeader.paid == values['paid'])
        if values.get('is_exception', None):
            conditions.append(OrderHeader.is_exception == values['is_exception'])
        if values.get('is_less_qty', None):
            conditions.append(OrderHeader.is_less_qty == values['is_less_qty'])


        # for the sort function
        field = values.get('field', 'create_time')
        if values.get('direction', 'desc') == 'desc':
            result = DBSession.query(OrderHeader).filter(and_(*conditions)).order_by(desc(getattr(OrderHeader, field)))
        else:
            result = DBSession.query(OrderHeader).filter(and_(*conditions)).order_by(getattr(OrderHeader, field))

        def url_for_page(**params): return url_for('bpOrder.view', action = "index", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        return {
                'values' : values ,
                'targets' : targets,
                'records' : records,
                'source_cites' : source_cites,
                'destination_cites' : destination_cites,
                }


    @templated('order/add.html')
    def add(self):
        ratios = {}
        for r in DBSession.query(Ratio).filter(Ratio.active == 0):
            ratios[r.type] = r.value
        return {
                'ratios' : ratios,
                }


    def save_new(self):
        try:
            code, header = self._save_new_process()

            for nk, nv in _gp('item_id_'):
                id = nk.split("_")[2]
                DBSession.add(ItemDetail(
                                         header = header, item_id = nv , qty = _g("item_qty_%s" % id) ,
                                         vol = _g("item_vol_%s" % id), weight = _g("item_weight_%s" % id)
                                         ))
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        except:
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            DBSession.rollback()

        return redirect(url_for('.view', action = 'index'))




    def _save_new_process(self):
        params = {}
        for k in [
#                  'source_station', 'destination_station',
                  'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                  'source_company_id', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                  'destination_company_id', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                  'ref_no', 'order_time', 'expect_time', 'actual_time', 'remark',
                 'payment_id', 'pickup_type_id', 'pack_type_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
                  'weight', 'weight_ratio', 'weight_ratio', 'amount', 'insurance_charge', 'sendout_charge', 'receive_charge',
                  'package_charge', 'other_charge', 'note_id', 'note_no',
                  'source_sms', 'destination_sms',
                  ]:
            params[k] = _g(k)
        order = OrderHeader(**params)
        DBSession.add(order)
        DBSession.flush()

        order.no = genSystemNo(order.id)
        order.barcode = generate_barcode_file(order.no)

        DBSession.add(TransferLog(
                                  refer_id = order.id,
                                  transfer_date = dt.now().strftime(SYSTEM_DATETIME_FORMAT),
                                  type = 0,
                                  remark = LOG_CREATE_ORDER,
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

        logs = []
        logs.extend(header.get_logs())
        try:
            deliver_detail = DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == header.id)).one()
            deliver_heaer = deliver_detail.header
            for f in deliver_heaer.get_logs() : _info(f.remark)
            logs.extend(deliver_heaer.get_logs())
        except:
#            _error(traceback.print_exc())
            pass
        logs = sorted(logs, cmp = lambda x, y: cmp(x.transfer_date, y.transfer_date))

        if header.source_company_id:
            targets = header.source_company.targets
        else:
            targets = {}

        if header.source_province_id:
            source_cites = header.source_province.children()
        else: source_cites = []

        if header.destination_province_id:
            destination_cites = header.destination_province.children()
        else: destination_cites = []

        return {
                'header' : header ,
                'transit_logs' : logs,
                'targets' : targets,
                'source_cites' : source_cites,
                'destination_cites' : destination_cites,
                }


    @templated('order/copy.html')
    def copy(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)

        logs = []
        logs.extend(header.get_logs())
        try:
            deliver_detail = DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == header.id)).one()
            deliver_heaer = deliver_detail.header
            for f in deliver_heaer.get_logs() : _info(f.remark)
            logs.extend(deliver_heaer.get_logs())
        except:
            pass

        sorted(logs, cmp = lambda x, y: cmp(x.transfer_date, y.transfer_date))

        if header.source_company_id:
            targets = header.source_company.targets
        else:
            targets = {}

        if header.source_province_id:
            source_cites = header.source_province.children()
        else: source_cites = []

        if header.destination_province_id:
            destination_cites = header.destination_province.children()
        else: destination_cites = []

        return {
                'header' : header ,
                'transit_logs' : logs,
                'targets' : targets,
                'source_cites' : source_cites,
                'destination_cites' : destination_cites,
                }


#
#    def save_update(self):
#        id = _g('id') or None
#        if not id :
#            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
#            return redirect(self.default())
#
#        header = DBSession.query(OrderHeader).get(id)
#        try:
#            for k in ['source_station', 'source_company', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
#                  'destination_station', 'destination_company', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
#                  'no', 'order_time', 'item', 'expect_time', 'remark',
#                 'payment_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
#                  'weight', 'weight_ratio', 'weight_ratio', 'amount',
#                  ]:
#                setattr(header, k, _g(k) or None)
#
#            DBSession.commit()
#        except:
#            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
#            DBSession.rollback()
#        else:
#            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
#            return redirect(url_for('.view', action = 'index'))



    def delete(self):
        header = getOr404(OrderHeader, _g('id'), redirect_url = self.default())
#        header.status = ORDER_CANCELLED[0]
        header.active = 1
        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))


#    def do_action(self):
#        header = OrderHeader.get(_g('id'))
#
#        if not header :
#            flash(MSG_RECORD_NOT_EXIST)
#            return redirect(self.default())
#
#        if _g('sc') == 'ASSIGN_PICKER' :
#            header.receiver = _g('receiver')
#            header.receiver_contact = _g('receiver_contact')
#            header.receiver_remark = _g('receiver_remark')
#            header.status = ASSIGN_PICKER[0]
#            for d in header.details: d.status = ASSIGN_PICKER[0]
#
#            DBSession.add(TransferLog(
#                                      refer_id = header.id,
#                                      transfer_date = dt.now().strftime("%Y-%m-%d"),
#                                      type = 0,
#                                      remark = LOG_SEND_PICKER
#                                      ))
#
#        elif _g('sc') == 'IN_WAREHOUSE' :
#            header.in_warehouse_remark = _g('in_warehouse_remark')
#            header.status = IN_WAREHOUSE[0]
#            location_id = _g('location_id')
#            for d in header.details:
#                d.status = IN_WAREHOUSE[0]
#
#                if location_id:
#                    DBSession.add(InventoryItem(
#                                                item = d.item,
#                                                location_id = location_id,
#                                                qty = d.order_qty,
#                                                refer_order_header = unicode(header),
#                                                refer_order_detail_id = d.id,
#                                                ))
#
#            DBSession.add(TransferLog(
#                                      refer_id = header.id,
#                                      transfer_date = dt.now().strftime("%Y-%m-%d"),
#                                      type = 0,
#                                      remark = LOG_GOODS_IN_WAREHOUSE
#                                      ))
#
#        DBSession.commit()
#        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
#        return redirect(self.default())


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
#    @templated('order/add_by_customer.html')
#    def add_by_customer(self):
#
#        if not session.get('customer_profile', None) or not session['customer_profile'].get('id', None):
#            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
#            return redirect(url_for('bpRoot.view', action = "index"))
#        return {
#                'units' : getMasterAll(ItemUnit),
#                'wunits' : getMasterAll(WeightUnit),
#                'shiptype' : getMasterAll(ShipmentType),
#                }


    #===========================================================================
    # not very important
    #===========================================================================
#    def save_new_by_customer(self):
#        code = self._save_new_process()
#        if code == 0:
#            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
#        else:
#            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
#        return redirect(url_for('.view', action = 'search_by_customer'))


#    @templated('order/search_by_customer.html')
#    def search_by_customer(self):
#        if not session.get('customer_profile', None) or not session['customer_profile'].get('id', None):
#            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
#            return redirect(url_for('bpRoot.view', action = "index"))
#        conditions = [OrderHeader.active == 0,
#                      OrderDetail.active == 0,
#                      OrderHeader.id == OrderDetail.header_id,
#                      OrderHeader.customer_id == session['customer_profile']['id'],
#                      ]
#        if _g('no'):
#            conditions.append(OrderHeader.no.like('%%%s%%' % _g('no')))
#        if _g('destination_address'):
#            conditions.append(OrderDetail.destination_address.like(_g('destination_address')))
#        if _g('create_time_from'):
#            conditions.append(OrderHeader.create_time > _g('create_time_from'))
#        if _g('create_time_to'):
#            conditions.append(OrderHeader.create_time < _g('create_time_to'))
#
#        result = DBSession.query(OrderHeader, OrderDetail).filter(and_(*conditions)).order_by(OrderHeader.no)
#        return {'result' : result, 'values' : {
#                                              'no' : _g('no'), 'destination_address' : _g('destination_address'),
#                                              'create_time_from' : _g('create_time_from'), 'create_time_to' : _g('create_time_to')
#                                              }}
#

#    @templated('order/search_transfer_log.html')
#    def search_transfer_log(self):
#        header = OrderHeader.get(_g('id'))
#
#        if not header :
#            flash(MSG_RECORD_NOT_EXIST)
#            return redirect(self.default())
#
#        order_log = header.get_logs()
#        detail_log = {}
#        for d in header.details:
#            logs = []
#            for dd in DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == d.id)).order_by(DeliverDetail.id):
#                logs.extend(dd.header.get_logs())
#            detail_log[d.id] = logs
#
#        return {'order_log' : order_log, 'detail_log' : detail_log}


    def ajax_todo_list(self):

        def f(v):
            result = []
            data = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0 , OrderHeader.status == v)).order_by(OrderHeader.create_time)
            for l in data[:5]:
                result.append({'id' : l.id, 'ref_no' : l.ref_no})
            return {'list' : result, 'count' : data.count()}

        try:
            data = {
                "orders_new" : f(ORDER_NEW[0]),
                "order_receiver" : f(ASSIGN_RECEIVER[0]),
                "order_inhouse" : f(IN_WAREHOUSE[0]),
                "order_sorted" : f(SORTING[0]),
                    }
            return jsonify(result = 0, data = data)
        except:
            _error(traceback.print_exc())
            return jsonify(result = 1, data = [])

    @templated('order/barcode.html')
    def print_barcode(self):
        header = OrderHeader.get(_g('id'))

        if not header :
            flash(MSG_RECORD_NOT_EXIST)
            return redirect(self.default())

        return {'header' : header}






    def ajax_save(self):
        type = _g('form_type')
        id = _g("id")
        if type not in ['order_header', 'item_detail', 'receiver', 'warehouse' , 'transit', 'signed', 'pickup']:
            return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})

        header = DBSession.query(OrderHeader).get(id)

        if type == 'order_header':
            fields = [
#                      'source_station', 'destination_station',
                      'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                      'ref_no', 'source_company_id', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                      'payment_id', 'qty', 'weight', 'vol', 'shipment_type_id',
                       'destination_company_id', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                      'order_time', 'expect_time', 'actual_time', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'amount', 'cost', 'remark',
                      'pickup_type_id', 'pack_type_id',
                      'insurance_charge', 'sendout_charge', 'receive_charge', 'package_charge', 'other_charge',
                      'note_id', 'note_no',
                      'source_sms', 'destination_sms',
                      ]
            for f in fields:
                setattr(header, f, _g(f))
            try:
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})
            except:
                _error(traceback.print_exc())
                DBSession.rollback()
                return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        elif type == 'item_detail':
            action_type = _g('action_type')
            if action_type not in ['ADD', 'DELETE']: return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action_type == 'ADD' :
                params = {'header' : header}
                for f in ['item_id', 'qty', 'vol', 'weight', 'remark', ]:
                    params[f] = _g(f)
                obj = ItemDetail(**params)
                DBSession.add(obj)
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC) , 'id' : obj.id})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

            else:
                line = DBSession.query(ItemDetail).get(_g('item_id'))
                line.active = 1
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        elif type == 'receiver' :
            for f in ['receiver_contact_id', 'receiver_tel', 'receiver_mobile', 'receiver_remark', ]:
                setattr(header, f, _g(f))

            if header.status < ASSIGN_RECEIVER[0]:
                header.update_status(ASSIGN_RECEIVER[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = dt.now().strftime(SYSTEM_DATETIME_FORMAT),
                                  type = 0,
                                  remark = LOG_SEND_RECEIVER + (u'收件人: %s , 收件人电话: %s , 收件人手机: %s, 备注:%s' % (header.receiver_contact, header.receiver_tel or '', header.receiver_mobile or '', header.receiver_remark or '')),
                                  ))
            try:
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})
            except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        elif type == 'warehouse' :
            action = _g('action')
            if action not in ['IN', 'OUT'] : return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action == 'IN' :
                header.update_status(IN_WAREHOUSE[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = _g('wh_time'),
                                  type = 0,
                                  remark = _g('wh_remark'),
                                  ))
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

            else:
                header.update_status(OUT_WAREHOUSE[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = _g('wh_time'),
                                  type = 0,
                                  remark = _g('wh_remark'),
                                  ))
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        elif type == 'transit':
            action_type = _g('action_type')
            if action_type not in ['ADD', 'DELETE'] : return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action_type == 'ADD':
                obj = TransferLog(
                                  refer_id = header.id,
                                  transfer_date = _g('action_time'),
                                  type = 0,
                                  remark = LOG_GOODS_IN_TRAVEL + (u'备注:%s' % (_g('remark') or '')),
                                  )
                DBSession.add(obj)
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC) , 'transit_id' : obj.id})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

            else:
                transit_id = _g('transit_id')
                obj = DBSession.query(TransferLog).get(transit_id)
                obj.active = 1
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        elif type == 'pickup':
            action_type = _g('action_type')
            if action_type not in ['ADD', 'DELETE'] : return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})
            if action_type == 'ADD' :
                params = {}
                for f in ['action_time', 'contact', 'tel', 'qty', 'remark']: params[f] = _g(f)
                obj = PickupDetail(header = header, **params)
                DBSession.add(obj)

                header.update_status(GOODS_PICKUP[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = _g('action_time'),
                                  type = 0,
                                  remark = LOG_GOODS_PICKUPED + (u'提货人: %s, 提货数量: %s , 备注:%s' % (obj.contact, obj.qty, (_g('remark') or ''))),
                                  ))
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC) , 'pickup_id' : obj.id})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})
            else:
                pickup_id = _g('pickup_id')
                obj = DBSession.query(PickupDetail).get(pickup_id)
                obj.active = 1
                try:
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        if type == 'signed':
            for f in ['signed_contact', 'signed_tel', 'signed_time', 'signed_remark', ]:
                setattr(header, f, _g(f))

            if header.status < GOODS_SIGNED[0]:
                header.update_status(GOODS_SIGNED[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = _g('signed_time'),
                                  type = 0,
                                  remark = LOG_GOODS_SIGNED + (u'签收人:%s , 签收人电话:%s , 签收时间:%s' % (header.signed_contact, header.signed_tel or '', header.signed_time)),
                                  ))
            try:
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})
            except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})


    def export(self):
        ids = _gl('order_ids')

        _info(ids)

        data = []
        for r in DBSession.query(OrderHeader).filter(OrderHeader.id.in_(ids)).order_by(OrderHeader.create_time):
            row = [r.create_time, r.ref_no, r.destination_station, r.destination_contact, r.qty, r.weight, r.destination_tel, '', ] #A - H
            deliver_header = r.get_deliver_header()
            if deliver_header :
                row.extend(['', deliver_header.no, deliver_header.sendout_time, '', '', deliver_header.expect_time, deliver_header.actual_time, '', ]) #I - P
            else:
                row.extend(['', '', '', '', '', '', '', '', ]) #I - P

            pickup_info = ['', '', '', '', '', '0.5', '', '', ]
            tmp_count = 0
            for index, d in enumerate(r.pickup_details):
                if index > 2: break
                if d.qty :
                    pickup_info[index + 1] = d.qty
                    tmp_count += d.qty
            pickup_info[4] = r.qty - tmp_count
            row.extend(pickup_info) #Q - X
            row.extend(['', '', '',
                        'Y' if r.actual_time > r.expect_time else 'N',
                        'Y' if r.signed_time else 'N',
                        r.signed_contact or '', r.signed_time, '', '', ]) #Y - AG

            data.append(row)

        if not data : data = [['', ], ]


        if not os.path.exists(TMP_FOLDER): os.makedirs(TMP_FOLDER)
        current = dt.now()
        templatePath = os.path.join(TEMPLATE_FOLDER, "template.xls")
        tempFileName = os.path.join(TMP_FOLDER, "report_tmp_%s_%d.xls" % (current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
        realFileName = os.path.join(TMP_FOLDER, "report_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))
        shutil.copy(templatePath, tempFileName)
        report_xls = SummaryReport(templatePath = tempFileName, destinationPath = realFileName)

        report_xls.inputData(data = data)
        report_xls.outputData()
        try:
            os.remove(tempFileName)
        except:
            pass
        return send_file(realFileName, as_attachment = True)



    def check_note(self):
        try:
            note_id = _g('note_id')
            note_no = _g('note_no')
            note = DBSession.query(Note).get(note_id)
            for (b, e) in note.range:
                _info(b)
                _info(e)
                _info(note_no)
                if b <= note_no <= e:
                    return jsonify({'code' : 0 , 'result' : 0})
            return jsonify({'code' : 0 , 'result' : 1})
        except:
            _error(traceback.print_exc())
            return jsonify({'code' : 1 , 'msg' : MSG_SERVER_ERROR})



    def ajax_change_flag(self):
        try:
            id = _g('id')
            flag = _g('flag')
            type = _g('type')
            r = DBSession.query(OrderHeader).get(id)
            if type == 'APPROVE':
                r.approve = flag
            elif type == 'PAID':
                r.paid = flag
            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : MSG_UPDATE_SUCC})
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            return jsonify({'code' : 1, 'msg' : MSG_SERVER_ERROR})




bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

