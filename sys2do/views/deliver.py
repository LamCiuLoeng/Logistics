# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-6
#  @author: cl.lam
#  Description:
###########################################
'''
import os
import traceback
from datetime import datetime as dt, timedelta
import random
import shutil


from flask import session
from flask import request
from flask.blueprints import Blueprint
from flask.views import View
from flask.helpers import url_for, flash, jsonify, send_file
from sqlalchemy.sql.expression import and_, desc
from werkzeug.utils import redirect
from webhelpers import paginate

from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION, MESSAGE_INFO, \
    MSG_SAVE_SUCC, IN_WAREHOUSE, MSG_UPDATE_SUCC, ORDER_NEW, \
    ORDER_CANCELLED, MSG_DELETE_SUCC, SORTING, MSG_RECORD_NOT_EXIST, SEND_OUT, \
    GOODS_ARRIVED, IN_TRAVEL, GOODS_SIGNED, MSG_SERVER_ERROR, LOG_GOODS_SORTED, \
    LOG_GOODS_SENT_OUT, LOG_GOODS_ARRIVAL, MSG_NO_ID_SUPPLIED, \
    SYSTEM_DATETIME_FORMAT, MSG_ORDER_NOT_FIT_FOR_DELIVER
from sys2do.util.decorator import templated, login_required, tab_highlight, \
    mark_path
from sys2do.model import DBSession
from sys2do.views import BasicView
from sys2do.model.logic import DeliverHeader, OrderHeader, \
    DeliverDetail, TransferLog
from sys2do.util.common import _gl, _g, _gp, getOr404, getMasterAll, _debug, \
    _error, _info, send_sms, upload, multiupload
from sys2do.model.master import Supplier, InventoryItem, Province, \
    SupplierDiquRatio, City
from sys2do.setting import PAGINATE_PER_PAGE, TMP_FOLDER, TEMPLATE_FOLDER
from sys2do.model.system import SystemLog
from sys2do.util.logic_helper import getDeliverNo
from sys2do.util.excel_helper import DeliverReport
from sys2do.model.auth import User



__all__ = ['bpDeliver']


bpDeliver = Blueprint('bpDeliver', __name__)

class DeliverView(BasicView):

    decorators = [login_required, tab_highlight('TAB_MAIN'), ]

    @templated('deliver/index.html')
    @mark_path('DELIVER_INDEX')
    def index(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['create_time_from', 'create_time_to', 'ref_no', 'destination_province_id',
                      'destination_city_id', 'supplier_id', 'order_no', ] :
                values[f] = _g(f)
            values['field'] = _g('field', None) or 'create_time'
            values['direction'] = _g('direction', None) or 'desc'

        else:  # come from paginate or return
            values = session.get('deliver_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1


        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['deliver_values'] = values

        conditions = [DeliverHeader.active == 0,
                      Supplier.id == DeliverHeader.supplier_id,
                      User.id == DeliverHeader.create_by_id]
        if values.get('create_time_from', None):
            conditions.append(DeliverHeader.order_time > values['create_time_from'])
        if values.get('create_time_to', None):
            conditions.append(DeliverHeader.order_time < '%s 23:59' % values['create_time_to'])
        if values.get('ref_no', None):
            conditions.append(DeliverHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values.get('destination_province_id', None):
            conditions.append(DeliverHeader.destination_province_id == values['destination_province_id'])
            dp = DBSession.query(Province).get(values['destination_province_id'])
            destination_cites = dp.children()
        else: destination_cites = []
        if values.get('destination_city_id', None):
            conditions.append(DeliverHeader.destination_city_id == values['destination_city_id'])
        if values.get('supplier_id', None):
            conditions.append(DeliverHeader.supplier_id == values['supplier_id'])

        if values.get('order_no', None):
            conditions.extend([
                               DeliverDetail.header_id == DeliverHeader.id,
                               DeliverDetail.active == 0,
                               OrderHeader.active == 0,
                               DeliverDetail.order_header_id == OrderHeader.id,
                               OrderHeader.ref_no.op('like')('%%%s%%' % values['order_no']),
                               ])

        # for the sort function
        field = values.get('field', 'create_time')
        if values.get('direction', 'desc') == 'desc':
            result = DBSession.query(DeliverHeader, Supplier, User).filter(and_(*conditions)).order_by(desc(getattr(DeliverHeader, field)))
        else:
            result = DBSession.query(DeliverHeader, Supplier, User).filter(and_(*conditions)).order_by(getattr(DeliverHeader, field))


        def url_for_page(**params): return url_for('bpDeliver.view', action = "index", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        return {
                'records' : records,
                'values' : values,
                'destination_cites' : destination_cites,
                }




    @templated('deliver/select_orders.html')
    def select_orders(self):
        result = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderHeader.status < SORTING[0])).all()
        return {'result' : result}



    def ajax_check_ids(self):
        action = _g('action')
        id = _g('id')
        if action not in ['ADD', 'DEL'] : return jsonify({'code' :-1 , 'msg' : unicode(MSG_NO_SUCH_ACTION)})
        if not id : return jsonify({'code' :-1 , 'msg' : unicode(MSG_NO_ID_SUPPLIED)})

        if action == 'ADD':
            if 'deliver_order_ids' in session: session['deliver_order_ids'].append(id)
            else: session['deliver_order_ids'] = [id, ]
            return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})
        else:
            if 'deliver_order_ids' not in session: pass
            else:
                try:
                    session['deliver_order_ids'].pop(session['deliver_order_ids'].index(id))
                except:
                    pass
                return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})


    @templated('deliver/add_deliver.html')
    def add_deliver(self):
        ids = _gl('order_ids')

        if not ids:
            ids = [_g('order_ids'), ]

        order_headers = DBSession.query(OrderHeader).filter(OrderHeader.id.in_(ids))
        if order_headers.count() == 1:
            h = order_headers[0]
            destination_province_id = h.destination_province_id
            destination_city_id = h.destination_city_id
            destination_address = h.destination_address
            destination_contact = h.destination_contact
            destination_tel = h.destination_tel
            destination_mobile = h.destination_mobile
            payment_id = h.payment_id
            pickup_type_id = h.pickup_type_id
        else:
            destination_province_id = destination_city_id = destination_address = destination_contact = destination_tel = destination_mobile = None
            payment_id = pickup_type_id = None

        total_qty = total_vol = total_weight = 0
        for h in order_headers:
            if h.status >= SORTING[0]:
                flash(MSG_ORDER_NOT_FIT_FOR_DELIVER, MESSAGE_ERROR)
                if request.referrer:
                    return redirect(request.referrer)
                else:
                    return redirect(self.default())
            else:
                total_qty += h.qty or 0
                total_vol += h.vol or 0
                total_weight += h.weight or 0


        suppliers = getMasterAll(Supplier)

        return {'result' : order_headers,
                'suppliers' : suppliers,
                'destination_province_id' : destination_province_id,
                'destination_city_id' : destination_city_id,
                'destination_address' : destination_address,
                'destination_contact' : destination_contact,
                'destination_tel' : destination_tel,
                'destination_mobile' : destination_mobile,
                'payment_id' : payment_id,
                'pickup_type_id' : pickup_type_id,
                'total_qty' : total_qty,
                'total_vol' : total_vol,
                'total_weight' : total_weight,
                }


    def deliver_save_new(self):
        try:
            params = {}
            for f in ['ref_no', 'destination_province_id', 'destination_city_id', 'destination_address', 'destination_contact',
                      'destination_tel', 'destination_mobile', 'supplier_id',
                      'supplier_contact', 'supplier_tel', 'expect_time', 'order_time',
                      'insurance_charge', 'sendout_charge', 'receive_charge', 'package_charge', 'load_charge', 'unload_charge',
                      'other_charge', 'proxy_charge', 'amount', 'payment_id', 'pickup_type_id', 'remark', 'carriage_charge',
                      'qty', 'weight', 'vol', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'shipment_type_id',
                      ]:
                params[f] = _g(f)
            header = DeliverHeader(**params)
            DBSession.add(header)
            DBSession.flush()
            header.no = getDeliverNo(header.id)
            total_qty = total_vol = total_weight = 0
            line_no = 1
            for k, id in _gp('detail_'):
                order_header = DBSession.query(OrderHeader).get(id)
                d = DeliverDetail(header = header,
                                            order_header = order_header,
                                            line_no = line_no,
                                            qty = _g('qty_%s' % id),
                                            vol = _g('vol_%s' % id),
                                            weight = _g('weight_%s' % id),
                                            insurance_charge = _g('insurance_charge_%s' % id),
                                            sendout_charge = _g('sendout_charge_%s' % id),
                                            receive_charge = _g('receive_charge_%s' % id),
                                            package_charge = _g('package_charge_%s' % id),
                                            load_charge = _g('load_charge_%s' % id),
                                            unload_charge = _g('unload_charge_%s' % id),
                                            other_charge = _g('other_charge_%s' % id),
                                            proxy_charge = _g('proxy_charge_%s' % id),
                                            carriage_charge = _g('carriage_charge_%s' % id),
                                            amount = _g('amount_%s' % id),
                                            )
                DBSession.add(d)
                if order_header.qty : total_qty += float(d.qty)
                if order_header.vol : total_vol += float(d.vol)
                if order_header.weight : total_weight += float(d.weight)

                order_header.update_status(SORTING[0])
                order_header.cost = _g('amount_%s' % id),
                order_header.deliver_header_ref = header.id
                order_header.deliver_header_no = header.ref_no
                line_no += 1

            header.qty = total_qty
            header.vol = total_vol
            header.weight = total_weight

            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = dt.now().strftime(SYSTEM_DATETIME_FORMAT),
                                      type = 1,
                                      remark = LOG_GOODS_SORTED
                                      ))

            # handle the upload file
            header.attachment = multiupload()
            DBSession.commit()
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(self.default())
        else:
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(self.default())

    @templated('deliver/view.html')
    def view(self):
        id = _g('id')
        h = DBSession.query(DeliverHeader).get(id)
        return {'header' : h, }


    @templated('deliver/view.html')
    def view_by_no(self):
        no = _g('no')
        try:
            h = DBSession.query(DeliverHeader).filter(and_(DeliverHeader.active == 0, DeliverHeader.no == no)).one()
            return {'header' : h, 'values' : h.populate() , 'details' : h.details}
        except:
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(self.default())


    @templated('deliver/revise.html')
    def revise(self):
        header = getOr404(DeliverHeader, _g('id'), redirect_url = self.default())

        if header.destination_province_id:
            destination_cites = header.destination_province.children()
        else: destination_cites = []
        return {'header' : header, 'destination_cites' : destination_cites}


    def deliver_save_revise(self):
        id = _g('id')
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        try:
            header = DBSession.query(DeliverHeader).get(id)
            fields = [
                      'ref_no', 'destination_province_id', 'destination_city_id', 'destination_address', 'destination_contact',
                      'destination_tel', 'destination_mobile', 'supplier_id', 'supplier_contact', 'supplier_tel',
                      'need_transfer', 'amount', 'remark', 'expect_time', 'order_time',
                      'insurance_charge', 'sendout_charge', 'receive_charge', 'package_charge', 'other_charge', 'carriage_charge',
                      'load_charge', 'unload_charge', 'proxy_charge', 'payment_id', 'pickup_type_id',
                      'qty', 'weight', 'vol', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'shipment_type_id',
                      ]

            _remark = []
            old_info = header.serialize(fields)  # to used for the history log
            for f in fields:    setattr(header, f, _g(f))

            total_qty = total_vol = total_weight = 0

            for d in header.details:
                d.qty = _g('qty_%s' % d.id)
                d.vol = _g('vol_%s' % d.id)
                d.weight = _g('weight_%s' % d.id)
                d.insurance_charge = _g('insurance_charge_%s' % d.id)
                d.sendout_charge = _g('sendout_charge_%s' % d.id)
                d.receive_charge = _g('receive_charge_%s' % d.id)
                d.package_charge = _g('package_charge_%s' % d.id)
                d.load_charge = _g('load_charge_%s' % d.id)
                d.unload_charge = _g('unload_charge_%s' % d.id)
                d.other_charge = _g('other_charge_%s' % d.id)
                d.proxy_charge = _g('proxy_charge_%s' % d.id)
                d.carriage_charge = _g('carriage_charge_%s' % d.id)
                d.amount = _g('amount_%s' % d.id)
                d.order_header.cost = d.amount

                if d.qty : total_qty += float(d.qty)
                if d.vol : total_vol += float(d.vol)
                if d.weight : total_weight += float(d.weight)


            header.qty = total_qty
            header.vol = total_vol
            header.weight = total_weight

            # handle the file upload
            old_attachment_ids = map(lambda (k, v) : v, _gp("old_attachment_"))
            old_attachment_ids.extend(multiupload())
            header.attachment = old_attachment_ids

            DBSession.commit()

            new_info = header.serialize(fields)
            change_result = header.compare(old_info, new_info)
            header.insert_system_logs(change_result)

            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(self.default())



    def delete(self):
        header = getOr404(DeliverHeader, _g('id'), redirect_url = self.default())
        header.active = 1

        for d in header.details:
            d.active = 1
            d.order_header.deliver_header_no = None
            d.order_header.deliver_header_ref = None
            d.order_header.status = ORDER_NEW[0]

        DBSession.add(SystemLog(
                                type = header.__class__.__name__,
                                ref_id = header.id,
                                remark = u'%s 删除送货该送货单。' % session['user_profile']['name']
                                ))

        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))


#    def do_action(self):
#        header = DeliverHeader.get(_g('id'))
#        if not header :
#            flash(MSG_RECORD_NOT_EXIST)
#            return redirect(self.default())
#
#        if _g('sc') not in ['SEND_OUT', 'GOODS_ARRIVED']:
#            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
#            return redirect(self.default())
#
#        try:
#            if _g('sc') == 'SEND_OUT' :
#                header.send_out_remark = _g('send_out_remark')
#                header.status = SEND_OUT[0]
#                for d in header.details :
#                    #delete the item form inventory
#                    for r in DBSession.query(InventoryItem).filter(and_(InventoryItem.active == 0, InventoryItem.refer_order_detail_id == d.order_detail_id)):
#                        r.active = 1
#
#
#                DBSession.add(TransferLog(
#                                      refer_id = header.id,
#                                      transfer_date = dt.now().strftime("%Y-%m-%d"),
#                                      type = 1,
#                                      remark = unicode(LOG_GOODS_SENT_OUT)
#                                      ))
#
#            elif _g('sc') == 'GOODS_ARRIVED':
#                header.actual_time = _g('actual_time')
#                header.arrived_remark = _g('arrived_remark')
#                header.update_status(GOODS_ARRIVED[0])
#                for d in header.details :
#                    d.order_detail.update_status(GOODS_ARRIVED[0])
#                    d.order_detail.actual_time = _g('actual_time')
#
#                DBSession.add(TransferLog(
#                                      refer_id = header.id,
#                                      transfer_date = dt.now().strftime("%Y-%m-%d"),
#                                      type = 1,
#                                      remark = LOG_GOODS_ARRIVAL
#                                      ))
#            DBSession.commit()
#        except:
#            DBSession.rollback()
#            _error(traceback.print_exc())
#            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
#            return redirect(self.default())
#        else:
#            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
#            return redirect(self.default())




#    def update_status(self):
#        header = getOr404(DeliverHeader, _g('id'))
#        status = int(_g('sc'))
#        (oheaders, odetails) = updateDeliverHeaderStatus(header.id, status)
#
#        if status == OUT_WAREHOUSE[0]: #remove the item from warehouse if it's out store action
#            for d in header.details:
#                record = DBSession.query(WarehouseItem).filter(WarehouseItem.order_detail_id == d.order_detail_id).one()
#                record.qty -= d.deliver_qty
#                if record.qty <= 0 : record.active = 1
#                d.order_detail.warehouse_qty -= d.deliver_qty
#
#        for oheader in oheaders:
#            DBSession.add(OrderLog(order = oheader, remark = _g('remark')))
#
#
#        DBSession.commit()
#        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
#        return redirect(self.default())


    @templated('deliver/vendor_select.html')
    def vendor_select(self):
        if not session.get('supplier_profile', None) or not session['supplier_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))
        result = DBSession.query(DeliverHeader).filter(and_(
                                                            DeliverHeader.active == 0,
                                                            DeliverHeader.status.in_([SEND_OUT[0], IN_TRAVEL[0], GOODS_ARRIVED[0]]),
                                                            DeliverHeader.supplier_id == session['supplier_profile']['id'],
                                                            )).order_by(DeliverHeader.create_time)
        return {'result' : result , 'values' : {
                                                'no' : _g('no'),
                                                'destination_address' : _g('destination_address'),
                                                'create_time_from' : _g('create_time_from'),
                                                'create_time_to' : _g('create_time_to'),
                                                }}

    @templated('deliver/vendor_input.html')
    def vendor_input(self):
        if not session.get('supplier_profile', None) or not session['supplier_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))

        header = DeliverHeader.get(_g('id'))
        if not header :
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))
        elif header.supplier_id != session['supplier_profile']['id']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))

        return {'values' : header.populate(), 'details' : header.details }


    def vendor_input_save(self):
        if not session.get('supplier_profile', None) or not session['supplier_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))


        header = DeliverHeader.get(_g('id'))
        if not header :
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))
        elif header.supplier_id != session['supplier_profile']['id']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))

        if _g('type') == "IN_TRAVEL" :
            new_status = IN_TRAVEL[0]
            remark = u'货物在途。备注 ：%s' % _g('remark')
        elif _g('type') == "GOODS_ARRIVED" :
            new_status = GOODS_ARRIVED[0]
            remark = u'货物到达。备注 ：%s' % _g('remark')
        elif _g('type') == "GOODS_SIGNED" :
            new_status = GOODS_SIGNED[0]
            remark = u'货物签收。备注 ：%s' % _g('remark')
        else:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))

        try:
            header.update_status(new_status)
            for d in header.details:
                d.order_detail.update_status(new_status)

#            log = DeliverLog(deliver_header_id = header.id, remark = _g('remark'))
#            DBSession.add(log)
            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = dt.now().strftime(SYSTEM_DATETIME_FORMAT),
                                      type = 1,
                                      remark = remark
                                      ))
            DBSession.commit()
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'vendor_select'))
        else:
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'vendor_select'))



    def _sms(self, header, suffix):
        try:
            for detail in header.details:
                order_header = detail.order_header
                users = []
                if order_header.source_sms and order_header.source_mobile:
                    users.append(order_header.source_mobile)
                if order_header.destination_sms and order_header.destination_mobile:
                    users.append(order_header.destination_mobile)
                if users:
                    content = u'订单:%s[目的站:%s，发货人:深福合力，收货人:%s，数量:%s件]%s' % (order_header.ref_no,
                                                                           order_header.destination_city or order_header.destination_province,
                                                                           order_header.destination_contact,
                                                                           order_header.qty, suffix)
                    send_sms(users, content)
        except:
            _error(traceback.print_exc())
            pass



    def ajax_save(self):
        id = _g("id")
        type = _g('form_type')
        if type not in ['sendout', 'transit', 'exception', 'arrived']:
            return jsonify({'code' :-1, 'msg' : unicode(MSG_NO_SUCH_ACTION)})

        header = DeliverHeader.get(id)
        if type == 'sendout':
            header.status = SEND_OUT[0]
            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = _g('send_out_time'),
                                      type = 1,
                                      remark = _g('send_out_remark')
                                      ))
            header.sendout_time = _g('send_out_time')

            DBSession.add(SystemLog(
                                    type = header.__class__.__name__,
                                    ref_id = header.id,
                                    remark = u'%s 确认该记录状态为已发货。' % session['user_profile']['name']
                                    ))


            DBSession.commit()
            self._sms(header, u'已发货。')
            return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})

        if type == 'transit':
            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = _g('transit_time'),
                                      type = 1,
                                      remark = _g('transit_remark')
                                      ))
            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})


        if type == 'arrived' :
            header.status = GOODS_ARRIVED[0]
            DBSession.add(TransferLog(
                                      refer_id = header.id,
                                      transfer_date = _g('arrived_time'),
                                      type = 1,
                                      remark = _g('arrived_remark')
                                      ))
            DBSession.add(SystemLog(
                                    type = header.__class__.__name__,
                                    ref_id = header.id,
                                    remark = u'%s 确认记录状态为货物已到达目的站。' % session['user_profile']['name']
                                    ))

            for d in header.details:
                order_header = d.order_header
                order_header.actual_time = _g('arrived_time')
            DBSession.commit()
            self._sms(header, u'已到达。')
            return jsonify({'code' : 0 , 'msg' : unicode(MSG_SAVE_SUCC)})



    def ajax_change_flag(self):
        try:
            id = _g('id')
            flag = _g('flag')
            type = _g('type')
            remark = None
            header = DBSession.query(DeliverHeader).get(id)

            if type == 'SUPLLIER_PAID':
                header.supplier_paid = flag
                if flag == '1':
                    remark = u'%s 确认该记录为已付款予承运商。' % session['user_profile']['name']
                else:
                    remark = u'%s 确认该记录为未付款予承运商。' % session['user_profile']['name']

                for d in header.details:
                    d.supplier_paid = flag
                    d.order_header.supplier_paid = flag
                    DBSession.add(SystemLog(
                                    type = d.order_header.__class__.__name__,
                                    ref_id = d.order_header_id,
                                    remark = remark
                                    ))

            DBSession.add(SystemLog(
                                    type = header.__class__.__name__,
                                    ref_id = header.id,
                                    remark = remark
                                    ))



            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : MSG_UPDATE_SUCC})
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            return jsonify({'code' : 1, 'msg' : MSG_SERVER_ERROR})



    def ajax_compute_ratio(self):
        province_id = _g('province_id')
        city_id = _g('city_id')
        supplier_id = _g('supplier_id')
        qty_ratio = ''
        weight_ratio = ''
        vol_ratio = ''

        q1 = DBSession.query(SupplierDiquRatio).filter(and_(SupplierDiquRatio.active == 0,
                                                           SupplierDiquRatio.supplier_id == supplier_id,
                                                           SupplierDiquRatio.province_id == province_id,
                                                           SupplierDiquRatio.city_id == city_id,
                                                           ))
        if q1.count() == 1 :
            t = q1.first()
            qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
        else:
            q2 = DBSession.query(SupplierDiquRatio).filter(and_(SupplierDiquRatio.active == 0,
                                                           SupplierDiquRatio.supplier_id == supplier_id,
                                                           SupplierDiquRatio.province_id == province_id,
                                                           SupplierDiquRatio.city_id == None,
                                                           ))
            if q2.count() == 1:
                t = q2.first()
                qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
            else:
                q3 = DBSession.query(City).filter(and_(City.active == 0, City.id == city_id))
                if q3.count() == 1:
                    t = q3.first()
                    qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
                else:
                    q4 = DBSession.query(Province).filter(and_(Province.active == 0, Province.id == province_id))
                    if q4.count() == 1:
                        t = q4.first()
                        qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio

        return jsonify({'code' : 0,
                        'qty_ratio' : qty_ratio,
                        'weight_ratio' : weight_ratio,
                        'vol_ratio' : vol_ratio})



    @templated('deliver/form.html')
    def form(self):
        id = _g('id')
        obj = DBSession.query(DeliverHeader).get(id)
        return {'obj' : obj}


    def export(self):
        values = {}
        for f in ['create_time_from', 'create_time_to', 'ref_no', 'order_no',
                  'destination_province_id', 'destination_city_id', 'supplier_id',
                  ] :
            values[f] = _g(f)

        conditions = [DeliverHeader.active == 0]
        if values.get('create_time_from', None):
            conditions.append(DeliverHeader.order_time > values['create_time_from'])
        if values.get('create_time_to', None):
            conditions.append(DeliverHeader.order_time < '%s 23:59' % values['create_time_to'])
        if values.get('ref_no', None):
            conditions.append(DeliverHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values.get('destination_province_id', None):
            conditions.append(DeliverHeader.destination_province_id == values['destination_province_id'])
        if values.get('destination_city_id', None):
            conditions.append(DeliverHeader.destination_city_id == values['destination_city_id'])
        if values.get('supplier_id', None):
            conditions.append(DeliverHeader.supplier_id == values['supplier_id'])

        if values.get('order_no', None):
            conditions.extend([
                               DeliverDetail.header_id == DeliverHeader.id,
                               DeliverDetail.active == 0,
                               OrderHeader.active == 0,
                               DeliverDetail.order_header_id == OrderHeader.id,
                               OrderHeader.ref_no.op('like')('%%%s%%' % values['order_no']),
                               ])
        data = []
        index = 1
        total_qty = total_weight = total_amount = total_vol = 0

        _f = lambda h : "/".join(map(lambda d : d.order_header.ref_no, h.details))
        _l = lambda h : "".join(map(unicode, [h.destination_province or '', h.destination_city or '']))

        q = DBSession.query(DeliverHeader).filter(and_(*conditions)).order_by(DeliverHeader.order_time)
        for dheader in q:
            row = [
                   index, _f(dheader), dheader.order_time, _l(dheader), dheader.supplier, dheader.ref_no, dheader.qty, dheader.weight, dheader.vol, dheader.amount,
                   dheader.payment, dheader.shipment_type or '',
                   ]
            data.append(map(lambda v : unicode(v), row))
            index += 1
            total_qty += dheader.qty or 0
            total_weight += dheader.weight or 0
            total_vol += dheader.vol or 0
            total_amount += dheader.amount or 0

        if not os.path.exists(TMP_FOLDER): os.makedirs(TMP_FOLDER)
        current = dt.now()
        templatePath = os.path.join(TEMPLATE_FOLDER, "deliver.xlsx")
        tempFileName = os.path.join(TMP_FOLDER, "report_tmp_%s_%d.xlsx" % (current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
        realFileName = os.path.join(TMP_FOLDER, "deliver_report_%s.xlsx" % (dt.now().strftime("%Y%m%d%H%M%S")))
        shutil.copy(templatePath, tempFileName)
        report_xls = DeliverReport(templatePath = tempFileName, destinationPath = realFileName)
        report_xls.inputData(data = data, total_qty = total_qty, total_weight = total_weight, total_vol = total_vol, total_amount = total_amount)
        report_xls.outputData()
        try:
            os.remove(tempFileName)
        except:
            pass
        return send_file(realFileName, as_attachment = True)


bpDeliver.add_url_rule('/', view_func = DeliverView.as_view('view'), defaults = {'action':'index'})
bpDeliver.add_url_rule('/<action>', view_func = DeliverView.as_view('view'))
