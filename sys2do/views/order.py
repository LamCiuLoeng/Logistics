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

from flask import Blueprint, render_template, url_for, session
from flask.views import View
from werkzeug.utils import redirect
from flask.helpers import flash

from sys2do.model.logic import OrderHeader, OrderDetail, TransferLog, \
    DeliverDetail
from sys2do.model import DBSession
from sys2do.util.decorator import templated, login_required
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, ORDER_CANCELLED, STATUS_LIST, IN_TRAVEL, \
    MSG_RECORD_NOT_EXIST, ASSIGN_PICKER, IN_WAREHOUSE, ASSIGN_PICKER, \
    LOG_CREATE_ORDER, LOG_SEND_PICKER, LOG_GOODS_IN_WAREHOUSE
from sys2do.views import BasicView
from sys2do.util.common import _g, getOr404, _gp, getMasterAll, _debug
from sys2do.model.master import CustomerProfile, WarehouseItem, Warehouse, \
    Customer, ItemUnit, WeightUnit, ShipmentType, Province, ChargeType
from sys2do.util.logic_helper import genSystemNo
from sqlalchemy.sql.expression import and_
from sys2do.util.barcode_helper import generate_barcode_file


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
        return {'customers' :getMasterAll(Customer),
                'units' : getMasterAll(ItemUnit),
                'wunits' : getMasterAll(WeightUnit),
                'shiptype' : getMasterAll(ShipmentType),
                'provinces' : getMasterAll(Province, 'id'),
                'chargetype' : getMasterAll(ChargeType),
                }


    def save_new(self):
        code = self._save_new_process()
        if code == 0:
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        else:
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view', action = 'index'))



    def _save_new_process(self):
        customer_id = _g('customer_id')
        source_province_id = _g('source_province_id')
        source_city_id = _g('source_city_id')
        source_district_id = _g('source_district_id')
        source_address = _g('source_address')
        source_tel = _g('source_tel')
        source_contact = _g('source_contact')
        remark = _g('remark')
        order = OrderHeader(no = None, customer_id = customer_id,
                            source_province_id = source_province_id, source_city_id = source_city_id, source_district_id = source_district_id,
                            source_address = source_address,
                            source_tel = source_tel, source_contact = source_contact, remark = remark)
        DBSession.add(order)

        item = _gp('item_')
        qty = _gp('qty_')
        unit = _gp('unit_')
        weight = _gp('weight_')
        wunit = _gp('wunit_')
        shipment_type = _gp('shipment_type_')
        province = _gp('destination_province_id_')
        city = _gp('destination_city_id_')
        district = _gp('destination_district_id_')
        dest = _gp('dest_')
        contact = _gp('contact_')
        tel = _gp('tel_')
        expect_time = _gp('expect_time_')
        charge = _gp('charge_')
        remark = _gp('remark_')


        line_no = 0

        _debug(item)
        _debug(qty)
        amount = 0

        for rItem, rQty, rUnit, rWeight, rWunit, rShip, rPro, rCity, rDis, rDest, rCon, rTel, rExp, rCh, rRem \
         in zip(item, qty, unit, weight, wunit, shipment_type, province, city, district, dest, contact, tel, expect_time, charge, remark):
            line_no += 1
            _debug(line_no)
            if rCh[1] : amount += float(rCh[1])
            DBSession.add(OrderDetail(header = order,
                                      line_no = line_no,
                                      item = rItem[1],
                                      order_qty = rQty[1],
                                      delivered_qty = 0,
                                      unit_id = rUnit[1],
                                      weight = rWeight[1],
                                      weight_unit_id = rWunit[1],
                                      shipment_type_id = rShip[1],
                                      destination_province_id = rPro[1],
                                      destination_city_id = rCity[1],
                                      destination_district_id = rDis[1],
                                      destination_address = rDest[1],
                                      destination_contact = rCon[1],
                                      destination_tel = rTel[1],
                                      expect_time = rExp[1],
                                      charge = rCh[1],
                                      remark = rRem[1]
                                      ))
        DBSession.flush()
        order.no = genSystemNo(order.id)
        order.barcode = generate_barcode_file(order.no)
        order.amount = amount
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
        app.logger.debug('go to review')
        header = getOr404(OrderHeader, _g('id'))
        app.logger.debug('go to review')
        values = header.populate()
        app.logger.debug('go to review')
        return {'values' : values , 'details' : header.details}


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
            for d in header.details: d.status = IN_WAREHOUSE[0]
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


    @templated('order/add_by_customer.html')
    def add_by_customer(self):
        if not session.get('customer_profile', None) or session['customer_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))
        return {
                'units' : getMasterAll(ItemUnit),
                'wunits' : getMasterAll(WeightUnit),
                'shiptype' : getMasterAll(ShipmentType),
                'provinces' : getMasterAll(Province, 'id'),
                }


    def save_new_by_customer(self):
        code = self._save_new_process()
        if code == 0:
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        else:
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view', action = 'search_by_customer'))


    @templated('order/search_by_customer.html')
    def search_by_customer(self):
        if not session.get('customer_profile', None) or session['customer_profile'].get('id', None):
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('bpRoot.view', action = "index"))
        conditions = [OrderHeader.active == 0, OrderDetail.active == 0, OrderHeader.id == OrderDetail.header_id]
        if _g('no'):
            conditions.append(OrderHeader.no.like('%%%s%%' % _g('no')))
        if _g('destination_address'):
            conditions.append(OrderDetail.destination_address == _g('destination_address'))
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
            for dd in DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_detail_id == d.id)).order_by(DeliverDetail.id):
                logs.extend(dd.header.get_logs())
            detail_log[d.id] = logs

        return {'order_log' : order_log, 'detail_log' : detail_log}



bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

