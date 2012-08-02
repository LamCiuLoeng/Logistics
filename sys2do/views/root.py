# -*- coding: utf-8 -*-
import traceback
import os
import random
from datetime import datetime as dt, timedelta
from flask import g, render_template, flash, session, redirect, url_for, request
from flask.blueprints import Blueprint
from flask.views import View
from flaskext.babel import gettext as _
from sqlalchemy import and_

from sys2do import app
from sys2do.model import DBSession, User
from flask.helpers import jsonify, send_file
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.util.common import _g, _gp, _gl, _info, _error
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, GOODS_PICKUP, GOODS_SIGNED, OUT_WAREHOUSE, IN_WAREHOUSE, \
    MSG_RECORD_NOT_EXIST, LOG_GOODS_PICKUPED, LOG_GOODS_SIGNED, MSG_SERVER_ERROR, \
    SYSTEM_DATE_FORMAT
from sys2do.views import BasicView
from sys2do.model.master import CustomerProfile, Customer, Supplier, \
    CustomerTarget, Receiver, CustomerTargetContact, Province, City, Barcode
from sys2do.model.logic import OrderHeader, TransferLog, PickupDetail
from sys2do.util.logic_helper import check_barcode


__all__ = ['bpRoot']

bpRoot = Blueprint('bpRoot', __name__)


class RootView(BasicView):

    @login_required
    @tab_highlight('TAB_HOME')
    @templated("index.html")
    def index(self):
    #    flash('hello!', MESSAGE_INFO)
    #    flash('SHIT!', MESSAGE_ERROR)
#        app.logger.debug('A value for debugging')
#        flash(TEST_MSG, MESSAGE_INFO)
#        return send_file('d:/new.png', as_attachment = True)
        return {}


    @login_required
    @tab_highlight('TAB_MAIN')
    @templated("main.html")
    def main(self):
        return {}


    @login_required
    @tab_highlight('TAB_DASHBOARD')
    @templated("dashboard.html")
    def dashboard(self):
        return {}


    def ajax_master(self):
        master = _g('m')
        if master == 'customer':
            cs = DBSession.query(Customer).filter(and_(Customer.active == 0, Customer.name.like('%%%s%%' % _g('name')))).order_by(Customer.name).all()

            data = [{'id' : c.id , 'name' : c.name } for c in cs]
            return jsonify({'code' : 0, 'msg' : '', 'data' : data})

        if master == 'customer_detail':
            c = DBSession.query(Customer).get(_g('id'))
            ts = [{'id' : t.id , 'name' : t.name } for t in c.targets]

            cities = []
            if _g('need_city_list', None) == '1' and c.province_id:
                cities = [{'id' : city.id, 'name' : city.name } for city in c.province.children()]

            return jsonify({'code' : 0 , 'msg' : '' , 'data' : c.populate() , 'targets' : ts, 'cities' : cities})

        if master == 'target':
            ts = DBSession.query(CustomerTarget).filter(and_(CustomerTarget.active == 0, CustomerTarget.customer_id == _g('id')))

            data = [{'id' : c.id , 'name' : c.name } for c in ts]
            return jsonify({'code' : 0, 'msg' : '', 'data' : data})

        if master == 'target_detail':
            t = DBSession.query(CustomerTarget).get(_g('id'))
            data = t.populate()
            if t.contact: data['contact'] = t.contact.populate()
            else : data['contact'] = {}

            cities = []
            if _g('need_city_list', None) == '1' and t.province_id:
                cities = [{'id' : city.id, 'name' : city.name } for city in t.province.children()]

            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data, 'cities' : cities})


        if master == 'target_contact_search':
            ts = DBSession.query(CustomerTargetContact).filter(and_(CustomerTargetContact.active == 0,
                                                               CustomerTargetContact.customer_target_id == _g('customer_target_id'),
                                                               CustomerTargetContact.name.op('like')("%%%s%%" % _g('customer_target_contact')),
                                                               )).all()
            data = [t.populate() for t in ts]
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data})

        if master == 'target_contact_detail':
            try:
                c = DBSession.query(CustomerTargetContact).filter(and_(CustomerTargetContact.active == 0,
                                                               CustomerTargetContact.name == _g('name'),
                                                               )).one()
                return jsonify({'code' : 0 , 'data' : c.populate()})
            except:
                return jsonify({'code' : 0 , 'data' : {}})


        if master == 'supplier':
            cs = DBSession.query(Supplier).filter(Supplier.active == 0).order_by(Supplier.name).all()
            return jsonify({'code' : 0, 'msg' : '', 'data' : cs})

        if master == 'supplier_detail':
            t = DBSession.query(Supplier).get(_g('id'))
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : t.populate()})

        if master == 'receiver_detail':
            t = DBSession.query(Receiver).get(_g('id'))
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : t.populate()})

        if master == 'province':
            ps = DBSession.query(Province).filter(and_(Province.active == 0)).order_by(Province.name)
            data = [{'id' : p.id, 'name' : p.name } for p in ps]
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data})

        if master == 'province_city':
            cs = DBSession.query(City).filter(and_(City.active == 0, City.parent_code == Province.code, Province.id == _g('pid'))).order_by(City.name)
            data = [{'id' : c.id, 'name' : c.name } for c in cs]
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data})

        return jsonify({'code' : 1, 'msg' : 'Error', })



    def _compose_xml_result(self, params):
        xml = []
        xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
        xml.append('<ORDER>')
        xml.append('<NO>%s</NO>' % params['no'])
        xml.append('<SOURCE_STATION>%s</SOURCE_STATION>' % params['source_station'])
        xml.append('<SOURCE_COMPANY>%s</SOURCE_COMPANY>' % params['source_company'])
        xml.append('<DESTINATION_STATION>%s</DESTINATION_STATION>' % params['destination_station'])
        xml.append('<DESTINATION_COMPANY>%s</DESTINATION_COMPANY>' % params['destination_company'])
        xml.append('<STATUS>%s</STATUS>' % params['status'])
        xml.append('</ORDER>')
        rv = app.make_response("".join(xml))
        rv.mimetype = 'text/xml'
        return rv

    def _compose_xml_response(self, code):
        xml = []
        xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
        xml.append('<RESULT>%s</RESULT>' % code)
        rv = app.make_response("".join(xml))
        rv.mimetype = 'text/xml'
        return rv


    def hh(self):
        type = _g('type')
        barcode = _g('barcode')

        if type == 'search':
            try:
                b = DBSession.query(Barcode).filter(and_(Barcode.active == 0, Barcode.value == barcode)).one()

                if b.status == 0 : # the barcode is used in a order
                    try:
                        h = DBSession.query(OrderHeader).filter(OrderHeader.no == barcode).one()
                        params = {
                                  'no' : h.ref_no,
                                  'source_station' : h.source_province,
                                  'source_company' : h.source_company,
                                  'destination_station' : h.destination_province,
                                  'destination_company' : h.destination_company,
                                  'status' : h.status,
                                  }
                    except:
                        _error(traceback.print_exc())
                        params = {
                          'no' : unicode(MSG_RECORD_NOT_EXIST),
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : ''
                          }
                elif b.status == 1 : # the barcode is reserved ,could be created a new order
                    params = {
                          'no' : 'BARCODE_AVAILABLE',
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : '-2'
                          }
                else: # the barcode is cancel ,equal not existed
                    params = {
                          'no' : unicode(MSG_RECORD_NOT_EXIST),
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : ''
                          }

            except:
                _error(traceback.print_exc())
                params = {
                          'no' : unicode(MSG_RECORD_NOT_EXIST),
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : ''
                          }

            return self._compose_xml_result(params)
        elif type == 'submit':
            try:
                action_type = _g('action_type')
                action_type = int(action_type)

                #create a draft order by the handheld
                if action_type == -2:
                    no = _g('barcode')
                    ref_no = _g('orderno')
                    try:
                        b = DBSession.query(Barcode).filter(Barcode.value == no).one()
                        if b.status != 1 :
                            return self._compose_xml_response(1)
                    except:
                        return self._compose_xml_response(1)

                    try:
                        DBSession.add(OrderHeader(no = no, ref_no = ref_no, status = -2))
                        b.status = 0
                        b.ref_no = ref_no
                        DBSession.commit()
                        return self._compose_xml_response(0)
                    except:
                        DBSession.rollback()
                        _error(traceback.print_exc())
                        return self._compose_xml_response(1)

                h = DBSession.query(OrderHeader).filter(OrderHeader.no == barcode).one()
                h.update_status(action_type)

                if action_type == IN_WAREHOUSE[0]:
                    remark = (u'订单: %s 确认入仓。备注：' % h.ref_no) + (_g('remark') or '')
                elif action_type == OUT_WAREHOUSE[0]:
                    remark = (u'订单: %s 确认出仓。备注：' % h.ref_no) + (_g('remark') or '')
                elif action_type == GOODS_SIGNED[0]:
                    remark = LOG_GOODS_SIGNED + (u'签收人:%s , 签收人电话:%s , 签收时间:%s' % (_g('contact'), _g('tel') or '', _g('time'))),
                    h.signed_time = _g('time')
                    h.signed_remark = _g('remark')
                    h.signed_contact = _g('contact')
                    h.signed_tel = _g('tel')
                elif action_type == GOODS_PICKUP[0]:
                    remark = LOG_GOODS_PICKUPED + (u'提货人: %s, 提货数量: %s , 备注:%s' % (_g('contact'), _g('qty'), (_g('remark') or ''))),
                    params = {
                              'action_time' : _g('time'),
                              'contact' : _g('contact'),
                              'qty' : _g('qty'),
                              'tel' : _g('tel'),
                              'remark' : _g('remark'),
                              }
                    obj = PickupDetail(header = h, **params)
                    DBSession.add(obj)

                DBSession.add(TransferLog(
                                  refer_id = h.id,
                                  transfer_date = _g('time'),
                                  type = 0,
                                  remark = remark,
                                  ))
                DBSession.commit()
                return self._compose_xml_response(0)
            except:
                return self._compose_xml_response(1)
        else:
            return self._compose_xml_response(MSG_NO_SUCH_ACTION)


    def sms(self):
        _info(request.values)
        return 'OK'


    def ajax_check_barcode(self):
        value = _g('value')
        (code, status) = check_barcode(value)

        return jsonify({'code' : code, 'status' : status})


    def compute_day_by_diqu(self):
        province_id = _g('province_id')
        city_id = _g('city_id')

        try:
            if city_id:
                c = DBSession.query(City).get(city_id)
                if c.shixiao:
                    result = dt.now() + timedelta(days = c.shixiao)
                    return jsonify({'code' : 0 , 'day' : result.strftime(SYSTEM_DATE_FORMAT)})
            elif province_id:
                p = DBSession.query(Province).get(province_id)
                if p.shixiao:
                    result = dt.now() + timedelta(days = p.shixiao)
                    return jsonify({'code' : 0 , 'day' : result.strftime(SYSTEM_DATE_FORMAT)})
            return jsonify({'code' : 0 , 'day' : dt.now().strftime(SYSTEM_DATE_FORMAT)})
        except:
            return jsonify({'code' : 1 , 'day' : ''})



bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
