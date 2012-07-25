# -*- coding: utf-8 -*-
import traceback
import os
import random
from datetime import datetime as dt
from flask import g, render_template, flash, session, redirect, url_for, request
from flask.blueprints import Blueprint
from flask.views import View
from flaskext.babel import gettext as _
from sqlalchemy import and_

from sys2do import app
from sys2do.model import DBSession, User
from flask.helpers import jsonify, send_file
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.util.common import _g, _gp, _gl
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, GOODS_PICKUP, GOODS_SIGNED, OUT_WAREHOUSE, IN_WAREHOUSE, \
    MSG_RECORD_NOT_EXIST, LOG_GOODS_PICKUPED, LOG_GOODS_SIGNED
from sys2do.views import BasicView
from sys2do.model.master import CustomerProfile, Customer, Supplier, \
    CustomerTarget, Receiver, CustomerTargetContact, Province, City
from sys2do.model.logic import OrderHeader, TransferLog, PickupDetail
from sys2do.util.logic_helper import genSystemNo


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
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : c.populate() , 'targets' : ts})

        if master == 'target':
            ts = DBSession.query(CustomerTarget).filter(and_(CustomerTarget.active == 0, CustomerTarget.customer_id == _g('id')))

            data = [{'id' : c.id , 'name' : c.name } for c in ts]
            return jsonify({'code' : 0, 'msg' : '', 'data' : data})

        if master == 'target_detail':
            t = DBSession.query(CustomerTarget).get(_g('id'))
            data = t.populate()
            if t.contact: data['contact'] = t.contact.populate()
            else : data['contact'] = {}
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data})

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



    def hh(self):
        type = _g('type')
        barcode = _g('barcode')

        if type == 'search':
            try:
                if barcode == '123456789':
                    params = {
                          'no' : 'BARCODE_AVAILABLE',
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : ''
                          }
                else:
                    h = DBSession.query(OrderHeader).filter(OrderHeader.no == barcode).one()
                    params = {
                              'no' : h.ref_no,
                              'source_station' : h.source_station,
                              'source_company' : h.source_company,
                              'destination_station' : h.destination_station,
                              'destination_company' : h.destination_company,
                              'status' : h.status,
                              }
            except:
                params = {
                          'no' : unicode(MSG_RECORD_NOT_EXIST),
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : ''
                          }

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
        elif type == 'submit':
            try:
                action_type = _g('action_type')
                action_type = int(action_type)
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
                xml = []
                xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
                xml.append('<RESULT>0</RESULT>')
                rv = app.make_response("".join(xml))
                rv.mimetype = 'text/xml'
                return rv
            except:
                xml = []
                xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
                xml.append('<RESULT>1</RESULT>')
                rv = app.make_response("".join(xml))
                rv.mimetype = 'text/xml'
                return rv
        else:
            xml = []
            xml.append('<?xml version="1.0" encoding="UTF-8" ?>')
            xml.append('<RESULT>%s</RESULT>' % MSG_NO_SUCH_ACTION)
            rv = app.make_response("".join(xml))
            rv.mimetype = 'text/xml'
            return rv

    @templated("index.html")
    def test(self):
        flash(GOODS_PICKUP[1], MESSAGE_ERROR)
        return {}

bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
