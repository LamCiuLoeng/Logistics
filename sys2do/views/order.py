# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-28
#  @author: cl.lam
#  Description:
###########################################
'''
import os
from datetime import datetime as dt
from datetime import timedelta
import traceback
import shutil
import random



from flask import Blueprint, render_template, url_for, session, Response
from flask.views import View
from werkzeug.utils import redirect
from flask.helpers import flash, jsonify, send_file

from sys2do.model.logic import OrderHeader, TransferLog, \
    DeliverDetail, ItemDetail, PickupDetail
from sys2do.model import DBSession
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, STATUS_LIST, IN_TRAVEL, \
    MSG_RECORD_NOT_EXIST, IN_WAREHOUSE, \
    LOG_CREATE_ORDER, LOG_GOODS_IN_WAREHOUSE, ORDER_NEW, \
    ASSIGN_RECEIVER, LOG_SEND_RECEIVER, OUT_WAREHOUSE, GOODS_PICKUP, \
    GOODS_SIGNED
from sys2do.views import BasicView
from sys2do.util.common import _g, getOr404, _gp, getMasterAll, _debug, _info, \
    _gl, _error
from sys2do.model.master import CustomerProfile, InventoryLocation, \
    Customer, ItemUnit, WeightUnit, ShipmentType, \
    InventoryItem, Payment, Ratio, PickupType, PackType
from sys2do.util.logic_helper import genSystemNo
from sqlalchemy.sql.expression import and_
from sys2do.util.barcode_helper import generate_barcode_file
from flask.globals import request
from sys2do.util.excel_helper import SummaryReport
from sys2do.setting import TMP_FOLDER, TEMPLATE_FOLDER




__all__ = ['bpOrder']

bpOrder = Blueprint('bpOrder', __name__)

class OrderView(BasicView):

    decorators = [login_required, tab_highlight('TAB_ORDER'), ]

    @templated('order/index.html')
#    @login_required
    def index(self):
        values = {}
        for f in ['create_time_from', 'create_time_to', 'ref_no', 'source_station', 'source_company', 'destination_station', 'destination_company'] :
            values[f] = _g(f)

        conditions = [OrderHeader.active == 0]
        if values['create_time_from']:
            conditions.append(OrderHeader.create_time > values['create_time_from'])
        if values['create_time_to']:
            conditions.append(OrderHeader.create_time < values['create_time_to'])
        if values['ref_no']:
            conditions.append(OrderHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values['source_station']:
            conditions.append(OrderHeader.source_station.op('like')('%%%s%%' % values['source_station']))
        if values['source_company']:
            conditions.append(OrderHeader.source_company.op('like')('%%%s%%' % values['source_company']))
        if values['destination_station']:
            conditions.append(OrderHeader.destination_station.op('like')('%%%s%%' % values['destination_station']))
        if values['destination_company']:
            conditions.append(OrderHeader.destination_company.op('like')('%%%s%%' % values['destination_company']))

        result = DBSession.query(OrderHeader).filter(and_(*conditions))

        total_qty = total_vol = total_weight = 0
        for r in result:
            if r.qty : total_qty += r.qty
            if r.vol : total_vol += r.vol
            if r.weight : total_weight += r.weight

        return {'result' : result , 'values' : values , 'total_qty' : total_qty , 'total_vol' : total_vol, 'total_weight' : total_weight}


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
                  'ref_no', 'order_time', 'item', 'item_remark', 'expect_time', 'remark',
                 'payment_id', 'pickup_type_id', 'pack_type_id', 'qty', 'qty_ratio', 'vol', 'vol_ratio',
                  'weight', 'weight_ratio', 'weight_ratio', 'amount',
                  ]:
            params[k] = _g(k)
        order = OrderHeader(**params)
        DBSession.add(order)
        DBSession.flush()

        order.no = genSystemNo(order.id)
        order.barcode = generate_barcode_file(order.no)

        DBSession.add(TransferLog(
                                  refer_id = order.id,
                                  transfer_date = dt.now().strftime("%Y-%m-%d"),
                                  type = 0,
                                  remark = u'新建订单',
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
            pass

        sorted(logs, cmp = lambda x, y: cmp(x.transfer_date, y.transfer_date))


        return {
                'header' : header ,
                'payment' : getMasterAll(Payment),
                'pickup_type' : getMasterAll(PickupType, 'id'),
                'pack_type' : getMasterAll(PackType, 'id'),
                'transit_logs' : logs
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
    def print_barcode(self):
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
        if type not in ['order_header', 'item_detail', 'receiver', 'warehouse' , 'transit', 'signed', 'pickup']:
            return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})

        header = DBSession.query(OrderHeader).get(id)

        if type == 'order_header':
            fields = ['ref_no', 'source_station', 'source_company', 'source_address', 'source_contact', 'source_tel', 'source_mobile',
                      'payment_id', 'item', 'qty', 'weight', 'vol', 'shipment_type_id',
                      'destination_station', 'destination_company', 'destination_address', 'destination_contact', 'destination_tel', 'destination_mobile',
                      'order_time', 'expect_time', 'actual_time', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'amount', 'cost', 'remark',
                      'pickup_type_id', 'pack_type_id',
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
                for f in ['item', 'qty', 'vol', 'weight', 'remark', ]:
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
            for f in ['receiver_contact', 'receiver_tel', 'receiver_mobile', 'receiver_remark', ]:
                setattr(header, f, _g(f))

            if header.status < ASSIGN_RECEIVER[0]:
                header.update_status(ASSIGN_RECEIVER[0])
                DBSession.add(TransferLog(
                                  refer_id = header.id,
                                  transfer_date = dt.now().strftime("%Y-%m-%d"),
                                  type = 0,
                                  remark = u'已派遣收件人收货。',
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
                                  remark = u'货物在途。' + (_g('remark') or ''),
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
                                  remark = u'订单已被提货。' + (_g('remark') or ''),
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
                                  remark = u'货物已签收。' + (_g('signed_remark') or ''),
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
            row = [r.create_time, r.no, r.destination_station, r.destination_contact, r.qty, r.weight, r.destination_tel, '', ] #A - H
            deliver_header = r.get_deliver_header()
            if deliver_header :
                row.extend(['', deliver_header.no, deliver_header.sendout_time, '', '', deliver_header.expect_time, deliver_header.actual_time, '', ]) #I - P
            else:
                row.extend(['', '', '', '', '', '', '', '', ]) #I - P

            pickup_info = ['', '', '', '', '', '0.5', '', '', ]
            tmp_count = 0
            for index, d in enumerate(r.pickup_details):
                if index > 2: break
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



bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

