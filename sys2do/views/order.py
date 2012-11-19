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
import json
from webhelpers import paginate
from werkzeug.utils import redirect
from flask import Blueprint, render_template, url_for, session, Response
from flask.globals import request
from flask.helpers import flash, jsonify, send_file
from flask.views import View
from sqlalchemy.sql.expression import and_, desc
from sqlalchemy.orm.exc import NoResultFound



from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, STATUS_LIST, IN_TRAVEL, MSG_RECORD_NOT_EXIST, \
    IN_WAREHOUSE, LOG_CREATE_ORDER, LOG_GOODS_IN_WAREHOUSE, ORDER_NEW, \
    ASSIGN_RECEIVER, LOG_SEND_RECEIVER, OUT_WAREHOUSE, GOODS_PICKUP, GOODS_SIGNED, \
    LOG_GOODS_SIGNED, LOG_GOODS_PICKUPED, LOG_GOODS_IN_TRAVEL, SORTING, \
    SYSTEM_DATETIME_FORMAT, ORDER_DRAFT
from sys2do.model import DBSession
from sys2do.model.logic import OrderHeader, TransferLog, DeliverDetail, \
    ItemDetail, PickupDetail
from sys2do.model.master import CustomerProfile, InventoryLocation, Customer, \
    ItemUnit, WeightUnit, ShipmentType, InventoryItem, Payment, Ratio, PickupType, \
    PackType, CustomerTarget, Receiver, Item, Note, City, Province, Barcode, \
    CustomerContact, CustomerSource
from sys2do.setting import TMP_FOLDER, TEMPLATE_FOLDER, PAGINATE_PER_PAGE
from sys2do.util.barcode_helper import generate_barcode_file
from sys2do.util.common import _g, getOr404, _gp, getMasterAll, _debug, _info, \
    _gl, _error, upload, multiupload
from sys2do.util.decorator import templated, login_required, tab_highlight, \
    mark_path
from sys2do.util.excel_helper import SummaryReport
from sys2do.views import BasicView
from sys2do.model.system import SystemLog
from sys2do.model.auth import User




__all__ = ['bpOrder']

bpOrder = Blueprint('bpOrder', __name__)

class OrderView(BasicView):

    decorators = [login_required, tab_highlight('TAB_MAIN'), ]

    @templated('order/index.html')
    @mark_path('ORDER_INDEX')
    def index(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['no', 'create_time_from', 'create_time_to', 'ref_no',
                      'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                      'customer_id', 'approve', 'paid', 'is_exception', 'is_less_qty'] :
                values[f] = _g(f)
            values['field'] = _g('field', None) or 'create_time'
            values['direction'] = _g('direction', None) or 'desc'

        else:  # come from paginate or return
            values = session.get('order_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1

        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['order_values'] = values

        conditions = [OrderHeader.active == 0,
                      Customer.id == OrderHeader.customer_id,
                      CustomerSource.id == OrderHeader.source_company_id,
                      CustomerTarget.id == OrderHeader.destination_company_id,
                      User.id == OrderHeader.create_by_id,
                      ]
        if values.get('create_time_from', None):
            conditions.append(OrderHeader.order_time > values['create_time_from'])
        if values.get('create_time_to', None):
            conditions.append(OrderHeader.order_time < '%s 23:59' % values['create_time_to'])
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

        if values.get('customer_id', None):
            conditions.append(OrderHeader.customer_id == values['customer_id'])

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
            result = DBSession.query(OrderHeader, Customer, CustomerSource, CustomerTarget, User)\
            .filter(and_(*conditions)).order_by(desc(getattr(OrderHeader, field)))
        else:
            result = DBSession.query(OrderHeader, Customer, CustomerSource, CustomerTarget, User)\
            .filter(and_(*conditions)).order_by(getattr(OrderHeader, field))

        def url_for_page(**params): return url_for('bpOrder.view', action = "index", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        return {
                'values' : values ,
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
            params = {}
            for k in ['customer_id', 'order_time',
                      'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                      'source_company_id', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                      'destination_company_id', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                      'ref_no', 'estimate_time', 'expect_time', 'actual_time', 'remark',
                      'payment_id', 'pickup_type_id', 'pack_type_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
                      'weight', 'weight_ratio', 'weight_ratio', 'amount', 'insurance_charge', 'sendout_charge', 'receive_charge',
                      'package_charge', 'other_charge', 'load_charge', 'unload_charge', 'proxy_charge', 'note_id', 'note_no',
                      'source_sms', 'destination_sms',
                      ]:
                params[k] = _g(k)
            order = OrderHeader(**params)
            DBSession.add(order)
            DBSession.flush()

            no = _g('no')
            b = Barcode.getOrCreate(no, order.ref_no)
            order.barcode = b.img
            order.no = b.value
            b.status = 0  # mark the barcode is use

            DBSession.add(TransferLog(
                                      refer_id = order.id,
                                      transfer_date = dt.now().strftime(SYSTEM_DATETIME_FORMAT),
                                      type = 0,
                                      remark = LOG_CREATE_ORDER,
                                      ))

            item_json = _g('item_json', '')
            for item in json.loads(item_json):
                DBSession.add(ItemDetail(
                                         header = order, item_id = item['item_id'], qty = item['qty'] or None,
                                         vol = item['vol'] or None, weight = item['weight'] or None,
                                         remark = item['remark'] or None
                                         ))


            # handle the upload file
            order.attachment = multiupload()

            # add the contact to the master
            try:
                DBSession.query(CustomerContact).filter(and_(
                                                         CustomerContact.active == 0,
                                                         CustomerContact.type == "S",
                                                         CustomerContact.refer_id == order.source_company_id,
                                                         CustomerContact.name == order.source_contact
                                                         )).one()
            except:
                # can't find the persons in source's contacts
                DBSession.add(CustomerContact(
                                              customer_id = order.customer_id,
                                              type = "S",
                                              refer_id = order.source_company_id,
                                              name = order.source_contact,
                                              address = order.source_address,
                                              phone = order.source_tel,
                                              mobile = order.source_mobile
                                              ))


            # add the contact to the master
            try:
                DBSession.query(CustomerContact).filter(and_(
                                                         CustomerContact.active == 0,
                                                         CustomerContact.type == "T",
                                                         CustomerContact.refer_id == order.destination_company_id,
                                                         CustomerContact.name == order.destination_contact
                                                         )).one()
            except:
                # can't find the persons in des's contacts
                DBSession.add(CustomerContact(
                                              customer_id = order.customer_id,
                                              type = "T",
                                              refer_id = order.destination_company_id,
                                              name = order.destination_contact,
                                              address = order.destination_address,
                                              phone = order.destination_tel,
                                              mobile = order.destination_mobile
                                              ))
            DBSession.commit()



            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'review', id = order.id))
        except:
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            DBSession.rollback()
            return redirect(self.default())



    def revise_by_barcode(self):
        barcode = _g('no')
        try:
            header = DBSession.query(OrderHeader).filter(OrderHeader.no == barcode).one()
            return redirect(url_for('.view', action = 'revise', id = header.id))
        except:
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for("bpRoot.view", action = "index"))


    @templated('order/review.html')
    def review(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        try:
            header = DBSession.query(OrderHeader).get(id)

            logs = []
            logs.extend(header.get_logs())
            try:
                deliver_detail = DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == header.id)).one()
                deliver_heaer = deliver_detail.header
    #            for f in deliver_heaer.get_logs() : _info(f.remark)
                logs.extend(deliver_heaer.get_logs())
            except:
                pass
            logs = sorted(logs, cmp = lambda x, y: cmp(x.transfer_date, y.transfer_date))

            return {
                    'header' : header ,
                    'transit_logs' : logs,
                    }
        except:
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return  redirect(self.default())


    @templated('order/revise.html')
    def revise(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())
        header = DBSession.query(OrderHeader).get(id)

        item_json = []
        for c in header.item_details:
            item_json.append({
                                "id" : "old_%s" % c.id,
                                "item_id" : c.item_id,
                                "qty" : c.qty,
                                "weight" : c.weight,
                                "vol" : c.vol,
                                "remark" : c.remark,
                                })
        return {'header' : header , 'item_json' : json.dumps(item_json)}


    def save_update(self):
        id = _g("id")
        if not id:
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())
        header = DBSession.query(OrderHeader).get(id)
        fields = [
                  'customer_id', 'order_time',
                  'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                  'ref_no', 'source_company_id', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                  'payment_id', 'qty', 'weight', 'vol', 'shipment_type_id',
                   'destination_company_id', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                  'estimate_time', 'expect_time', 'actual_time', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'amount', 'cost', 'remark',
                  'pickup_type_id', 'pack_type_id',
                  'insurance_charge', 'sendout_charge', 'receive_charge', 'package_charge', 'other_charge', 'load_charge', 'unload_charge',
                  'proxy_charge', 'note_id', 'note_no',
                  'source_sms', 'destination_sms',
                  ]
        _remark = []
        old_info = header.serialize(fields)  # to used for the history log

        checkbox_fields = ['source_sms', 'destination_sms', ]
        try:
            for f in fields: setattr(header, f, _g(f))

            for f in checkbox_fields:
                vs = _gl(f)
                if vs : setattr(header, f, vs[0])
                else : setattr(header, f, None)
            no = _g('no')
            if no != header.no:
                try:
                    old_barcode = DBSession.query(Barcode).filter(Barcode.value == header.no).one()
                    old_barcode.status = 1  # mark the old barcode to be reserved
                except:
                    pass
                try:
                    new_barcode = DBSession.query(Barcode).filter(Barcode.value == no).one()
                    new_barcode.status = 0  # mark the new barcode to be used
                except NoResultFound :
                    DBSession.add(Barcode(value = no))
                except:
                    pass
                header.no = no
                header.barcode = generate_barcode_file(header.no)

            if header.status == -2 : header.status = 0

            item_ids = [c.id for c in header.item_details]
            item_json = _g('item_json', '')
            for c in json.loads(item_json):
                if not c.get('id', None) : continue
                if isinstance(c['id'], basestring) and c['id'].startswith("old_"):  # existing item
                    cid = c['id'].split("_")[1]
                    t = DBSession.query(ItemDetail).get(cid)
                    t.item_id = c.get('item_id', None)
                    t.qty = c.get('qty', None)
                    t.weight = c.get('weight', None)
                    t.vol = c.get('vol', None)
                    t.remark = c.get('remark', None)
                    item_ids.remove(t.id)
                else:
                    DBSession.add(ItemDetail(
                                                header = header,
                                                item_id = c.get('item_id', None),
                                                qty = c.get('qty', None),
                                                weight = c.get('weight', None),
                                                vol = c.get('vol', None),
                                                remark = c.get('remark', None),
                                                  ))

            DBSession.query(ItemDetail).filter(ItemDetail.id.in_(item_ids)).update({'active' : 1}, False)

            # handle the file upload
            old_attachment_ids = map(lambda (k, v) : v, _gp("old_attachment_"))
            old_attachment_ids.extend(multiupload())
            header.attachment = old_attachment_ids

            DBSession.commit()

            # handle the system log
            new_info = header.serialize(fields)
            change_result = header.compare(old_info, new_info)
            header.insert_system_logs(change_result)
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view', action = 'review', id = header.id))




    @templated('order/copy.html')
    def copy(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)

        item_json = []
        for c in header.item_details:
            item_json.append({
                                "id" : "old_%s" % c.id,
                                "item_id" : c.item_id,
                                "qty" : c.qty,
                                "weight" : c.weight,
                                "vol" : c.vol,
                                "remark" : c.remark,
                                })
        return {'header' : header , 'item_json' : json.dumps(item_json)}



    def delete(self):
        header = getOr404(OrderHeader, _g('id'), redirect_url = self.default())
        header.active = 1
        DBSession.add(SystemLog(
                                type = header.__class__.__name__,
                                ref_id = header.id,
                                remark = u"%s 删除该记录。" % session['user_profile']['name'],
                                ))
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
                "order_draft" : f(ORDER_DRAFT[0]),
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
        if type not in ['item_detail', 'receiver', 'warehouse' , 'transit', 'signed', 'pickup']:
            return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})

        header = DBSession.query(OrderHeader).get(id)

        if type == 'item_detail':
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
                    DBSession.add(SystemLog(
                                        type = header.__class__.__name__,
                                        ref_id = header.id,
                                        remark = u'%s 删除货物记录[id : %s]。' % (session['user_profile']['name'], line.id)
                                        ))
                    DBSession.commit()
                    return jsonify({'code' : 0 , 'msg' : unicode(MSG_DELETE_SUCC)})
                except:
                    DBSession.rollback()
                    return jsonify({'code' : 1 , 'msg' : unicode(MSG_SERVER_ERROR)})

        elif type == 'receiver' :
            _remark = []
            for f in ['receiver_contact_id', 'receiver_tel', 'receiver_mobile', 'receiver_remark', ]:
                old_v = getattr(header, f)
                new_v = _g(f)
                if unicode(old_v) != unicode(new_v):  _remark.append(u"[%s]'%s' 修改为 '%s'" % (f, old_v, new_v))
                setattr(header, f, _g(f))
            DBSession.add(SystemLog(
                                    type = header.__class__.__name__,
                                    ref_id = header.id,
                                    remark = u"%s 修改该记录。修改内容为:%s" % (session['user_profile']['name'], ";".join(_remark))
                                    ))
            if header.status < ASSIGN_RECEIVER[0]:
                header.update_status(ASSIGN_RECEIVER[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = dt.now().strftime(SYSTEM_DATETIME_FORMAT),
                                  type = 0,
                                  remark = LOG_SEND_RECEIVER + (u'收件人: %s , 收件人电话: %s , 收件人手机: %s, 备注:%s' % (header.receiver_contact, header.receiver_tel or '', header.receiver_mobile or '', header.receiver_remark or '')),
                                  ))
                DBSession.add(SystemLog(
                                        type = header.__class__.__name__,
                                        ref_id = header.id,
                                        remark = u'%s 确认该记录状态为已指派收件人。' % session['user_profile']['name']
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
                DBSession.add(SystemLog(
                                        type = header.__class__.__name__,
                                        ref_id = header.id,
                                        remark = u'%s 确认该记录的状态为已入仓。' % session['user_profile']['name']
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
                DBSession.add(SystemLog(
                                        type = header.__class__.__name__,
                                        ref_id = header.id,
                                        remark = u'%s 确认该记录的状态为已出仓。' % session['user_profile']['name']
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
                    DBSession.add(SystemLog(
                                            type = obj.__class__.__name__,
                                            ref_id = header.id,
                                            remark = u'%s 删除该运输记录[id : %s]。' % (session['user_profile']['name'], obj.id)
                                            ))
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
                    DBSession.add(SystemLog(
                                            type = obj.__class__.__name__,
                                            ref_id = header.id,
                                            remark = u'%s 删除该提货记录[id : %s]。' % (session['user_profile']['name'], obj.id)
                                            ))
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
                DBSession.add(SystemLog(
                                        type = header.__class__.__name__,
                                        ref_id = header.id,
                                        remark = u'%s 确认该记录状态为已签收。' % session['user_profile']['name']
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

        def _f(obj):
            if obj.destination_city_id:
                return "".join(map(lambda v : unicode(v), [obj.destination_province, obj.destination_city]))
            return unicode(obj.destination_province)

        data = []
        for r in DBSession.query(OrderHeader).filter(OrderHeader.id.in_(ids)).order_by(OrderHeader.create_time):
            row = [r.order_time, r.ref_no, _f(r), unicode(r.destination_company), r.destination_contact, r.qty, r.weight, r.destination_tel, '', ]  # A - H
            deliver_header = r.get_deliver_header()
            if deliver_header :
                row.extend(['', deliver_header.no, deliver_header.sendout_time, '', '', deliver_header.expect_time, deliver_header.actual_time, '', ])  # I - P
            else:
                row.extend(['', '', '', '', '', '', '', '', ])  # I - P

            pickup_info = ['', '', '', '', '', '0.5', '', '', ]
            tmp_count = 0
            for index, d in enumerate(r.pickup_details):
                if index > 2: break
                if d.qty :
                    pickup_info[index + 1] = d.qty
                    tmp_count += d.qty
            pickup_info[4] = r.qty - tmp_count
            row.extend(pickup_info)  # Q - X
            row.extend(['', '', '',
                        'Y' if r.actual_time > r.expect_time else 'N',
                        'Y' if r.signed_time else 'N',
                        r.signed_contact or '', r.signed_time, '', '', ])  # Y - AG

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



    def ajax_check_before_save(self):
        try:
            note_id = _g('note_id')
            note_no = _g('note_no')
            note = DBSession.query(Note).get(note_id)
            note_no = int(note_no)
            if not (int(note.begin_no) <= int(note_no) <= int(note.end_no)):
                return jsonify({'code' : 0 , 'result' : 1, 'msg' : u'该票据不在可用范围内(%s~%s)，请修改！' % (note.begin_no, note.end_no)})

            ref_no = _g('ref_no')
            if DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderHeader.ref_no == ref_no)).count() > 0:
                return jsonify({'code' : 0 , 'result' : 1, 'msg' : u'已经存在重复的订单号码！'})

            return jsonify({'code' : 0 , 'result' : 0})
        except:
            _error(traceback.print_exc())
            return jsonify({'code' : 1 , 'msg' : MSG_SERVER_ERROR})



    def ajax_change_flag(self):
        try:
            ids = _g('order_ids')
            if not ids : return jsonify({'code' : 1, 'msg' : MSG_NO_ID_SUPPLIED})
            flag = _g('flag')
            action_type = _g('type')
            remark = None
            r = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderHeader.id.in_(ids.split("|"))))

            def _update(result, attr, value):
                for t in result : setattr(t, attr, value)

            if action_type == 'APPROVE':
                _update(r, "approve", flag)
                if flag == '1':  # approve
                    remark = u'%s 审核通过该订单。' % session['user_profile']['name']
                else:  # disapprove
                    remark = u'%s 审核不通过该订单。' % session['user_profile']['name']
            elif action_type == 'PAID':
                _update(r, "paid", flag)
                if flag == '1':
                    remark = u'%s 确认该订单为客户已付款。' % session['user_profile']['name']
                else:
                    remark = u'%s 确认该订单为客户未付款。' % session['user_profile']['name']
            elif action_type == 'SUPLLIER_PAID':
                _update(r, "supplier_paid", flag)
                if flag == '1':
                    remark = u'%s 确认该订单为已付款予承运商。' % session['user_profile']['name']
                else:
                    remark = u'%s 确认该订单为未付款予承运商。' % session['user_profile']['name']
            elif action_type == 'ORDER_RETURN':
                _update(r, "is_return_note", flag)
                if flag == '1':
                    remark = u'%s 确认该订单为客户已返回单。' % session['user_profile']['name']
                else:
                    remark = u'%s 确认该订单为客户未返回单。' % session['user_profile']['name']
            elif action_type == 'EXCEPTION':
                _update(r, "is_exception", flag)
                if flag == '1':
                    remark = u'%s 标记该订单为异常。' % session['user_profile']['name']
                else:
                    remark = u'%s 取消该订单的异常标记。' % session['user_profile']['name']
            elif action_type == 'LESS_QTY':
                _update(r, "is_less_qty", flag)
                if flag == '1':
                    remark = u'%s 标记该订单为少货。' % session['user_profile']['name']
                else:
                    remark = u'%s 取消该订单的少货标记。' % session['user_profile']['name']

            for t in r:
                DBSession.add(SystemLog(
                                    type = t.__class__.__name__,
                                    ref_id = t.id,
                                    remark = remark
                                    ))
            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : MSG_UPDATE_SUCC})
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            return jsonify({'code' : 1, 'msg' : MSG_SERVER_ERROR})



    def _compareObject(self, old_obj, new_obj):
        old_keys = old_obj.keys()
        new_keys = new_obj.keys()
        result = {
                  "new" : [],
                  "update" : [],
                  "delete" : [],
                  }

        for key in list(set(old_keys).intersection(set(new_keys))):
            old_val = old_obj[key][0]
            new_val = new_obj[key][0]

            if old_val != new_val:
                result['update'].append((old_obj[key][1], old_obj[key][0], new_obj[key][0]))

        for key in list(set(old_obj).difference(set(new_obj))):
            result['delete'].append((old_obj[key][1], old_obj[key][0], None))

        for key in list(set(new_obj).difference(set(old_obj))):
            result['new'].append((old_obj[key][1], None, new_obj[key][0]))
        return result


    @templated('order/form.html')
    def form(self):
        id = _g('id')
        header = DBSession.query(OrderHeader).get(id)
        return {'obj' : header}

bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

