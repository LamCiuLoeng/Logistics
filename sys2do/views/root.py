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
from flask.helpers import jsonify, send_file, send_from_directory
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.util.common import _g, _gp, _gl, _info, _error, date2text, _debug, \
    with_session, use_db_session, mywith
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC, GOODS_PICKUP, GOODS_SIGNED, OUT_WAREHOUSE, IN_WAREHOUSE, \
    MSG_RECORD_NOT_EXIST, LOG_GOODS_PICKUPED, LOG_GOODS_SIGNED, MSG_SERVER_ERROR, \
    SYSTEM_DATE_FORMAT, MSG_WRONG_PASSWORD, MSG_UPDATE_SUCC
from sys2do.views import BasicView
from sys2do.model.master import CustomerProfile, Customer, Supplier, \
    CustomerTarget, Receiver, CustomerContact, Province, City, Barcode, \
    CustomerDiquRatio, CustomerSource, InventoryItem
from sys2do.model.logic import OrderHeader, TransferLog, PickupDetail, \
    DeliverDetail
from sys2do.model.system import UploadFile
from sys2do.setting import UPLOAD_FOLDER_PREFIX




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
    @tab_highlight('TAB_MAIN')
    @templated("change_pw.html")
    def change_pw(self):
        return {}

    @login_required
    def save_pw(self):
        old_pw = _g('old_pw')
        new_pw = _g('new_pw')
        new_repw = _g('new_repw')

        msg = []
        if not old_pw : msg.push(u'请填写原始密码')
        if not new_pw : msg.push(u'请填写新密码')
        if not new_repw : msg.push(u'请填写确认密码')
        if new_pw != new_repw : msg.push(u'新密码与确认密码不相符！')

        if len(msg) > 0 :
            flash("\n".join(msg), MESSAGE_ERROR)
            return redirect('/change_pw')

        user = DBSession.query(User).get(session['user_profile']['id'])
        if not user.validate_password(old_pw):
            flash(u'原始密码错误！', MESSAGE_ERROR)
            return redirect('/change_pw')

        user.password = new_pw
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect('/index')


    @login_required
    @tab_highlight('TAB_DASHBOARD')
    @templated("dashboard.html")
    def dashboard(self):
        return {}



    def download(self):
        id = _g("id")
        f = DBSession.query(UploadFile).get(id)
        _debug(f.path)

        return send_file(os.path.join(UPLOAD_FOLDER_PREFIX, f.path), as_attachment = True, attachment_filename = f.name)





    def ajax_master(self):
        master = _g('m')
        if master == 'customer':
            cs = DBSession.query(Customer).filter(and_(Customer.active == 0, Customer.name.like('%%%s%%' % _g('name')))).order_by(Customer.name).all()

            data = [{'id' : c.id , 'name' : c.name } for c in cs]
            return jsonify({'code' : 0, 'msg' : '', 'data' : data})

        if master == 'customer_detail':
            c = DBSession.query(Customer).get(_g('id'))
            ss = [{'id' : s.id , 'name' : s.name } for s in c.sources]
            ts = [{'id' : t.id , 'name' : t.name } for t in c.targets]


            return jsonify({'code' : 0 , 'msg' : '' ,
                            'data' : c.populate() ,
                            'sources' : ss,
                            'targets' : ts,
                            })


        if master == 'source':
            ts = DBSession.query(CustomerSource).filter(and_(CustomerSource.active == 0, CustomerSource.customer_id == _g('id')))
            data = [{'id' : c.id , 'name' : c.name } for c in ts]
            return jsonify({'code' : 0, 'msg' : '', 'data' : data})


        if master == 'source_detail':
            s = DBSession.query(CustomerSource).get(_g('id'))
            data = s.populate()

            if s.default_contact() : data['contact'] = s.default_contact().populate()
            else: data['contact'] = {}

            cities = []
            if _g('need_city_list', None) == '1' and s.province_id:
                cities = [{'id' : city.id, 'name' : city.name } for city in s.province.children()]
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data, 'cities' : cities})


        if master == 'target':
            ts = DBSession.query(CustomerTarget).filter(and_(CustomerTarget.active == 0, CustomerTarget.customer_id == _g('id')))

            data = [{'id' : c.id , 'name' : c.name } for c in ts]
            return jsonify({'code' : 0, 'msg' : '', 'data' : data})

        if master == 'target_detail':
            t = DBSession.query(CustomerTarget).get(_g('id'))
            data = t.populate()
            if t.default_contact(): data['contact'] = t.default_contact().populate()
            else : data['contact'] = {}

            cities = []
            if _g('need_city_list', None) == '1' and t.province_id:
                cities = [{'id' : city.id, 'name' : city.name } for city in t.province.children()]

            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data, 'cities' : cities})


        if master == 'contact_search':
            ts = DBSession.query(CustomerContact).filter(and_(CustomerContact.active == 0,
                                                              CustomerContact.type == _g('type'),
                                                              CustomerContact.refer_id == _g('refer_id'),
                                                              CustomerContact.name.op('like')("%%%s%%" % _g('customer_contact')),
                                                               )).all()
            data = [t.populate() for t in ts]
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : data})


        if master == 'target_contact_detail':
            try:
                c = DBSession.query(CustomerContact).filter(and_(CustomerContact.active == 0,
                                                               CustomerContact.name == _g('name'),
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

        if master == 'inventory_item':
            t = DBSession.query(InventoryItem).get(_g('id'))
            return jsonify({'code' : 0 , 'msg' : '' , 'data' : t.populate()})

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

                if b.status == 0 :  # the barcode is used in a order
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
                elif b.status == 1 :  # the barcode is reserved ,could be created a new order
                    params = {
                          'no' : 'BARCODE_AVAILABLE',
                          'source_station' : '',
                          'source_company' : '',
                          'destination_station' : '',
                          'destination_company' : '',
                          'status' : '-2'
                          }
                else:  # the barcode is cancel ,equal not existed
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

                # create a draft order by the handheld
                if action_type == -2:
                    no = _g('barcode')
                    ref_no = _g('orderno')

                    b = Barcode.getOrCreate(no, ref_no, status = 0)
                    try:
                        DBSession.add(OrderHeader(no = no, ref_no = ref_no, status = -2))
                        b.status = 0
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
        (code, status) = Barcode.check(value)

        return jsonify({'code' : code, 'status' : status})


    def compute_by_diqu(self):
        province_id = _g('province_id')
        city_id = _g('city_id')
        customer_id = _g('customer_id')

        # count the ratio
        ratio_result = self._compute_ratio(customer_id, province_id, city_id)
        # count the day
        day_result = self._compute_day(province_id, city_id)

        ratio_result.update(day_result)
        ratio_result.update({'code' : 0})
        return jsonify(ratio_result)


    def _compute_day(self, province_id, city_id):
        estimate_day = ''
        if city_id:
            c = DBSession.query(City).get(city_id)
            if c.shixiao:
                estimate_day = (dt.now() + timedelta(days = c.shixiao)).strftime(SYSTEM_DATE_FORMAT)
            else:
                p = DBSession.query(Province).get(province_id)
                if p.shixiao:
                    estimate_day = (dt.now() + timedelta(days = p.shixiao)).strftime(SYSTEM_DATE_FORMAT)
        elif province_id:
            p = DBSession.query(Province).get(province_id)
            if p.shixiao:
                estimate_day = (dt.now() + timedelta(days = p.shixiao)).strftime(SYSTEM_DATE_FORMAT)
        return {'day' : estimate_day}



    def _compute_ratio(self, customer_id, province_id, city_id):
        qty_ratio = ''
        weight_ratio = ''
        vol_ratio = ''

        q1 = DBSession.query(CustomerDiquRatio).filter(and_(CustomerDiquRatio.active == 0,
                                                           CustomerDiquRatio.customer_id == customer_id,
                                                           CustomerDiquRatio.province_id == province_id,
                                                           CustomerDiquRatio.city_id == city_id,
                                                           ))

        if q1.count() == 1:
            t = q1.one()
            qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
        else:
            q2 = DBSession.query(CustomerDiquRatio).filter(and_(CustomerDiquRatio.active == 0,
                                                           CustomerDiquRatio.customer_id == customer_id,
                                                           CustomerDiquRatio.province_id == province_id,
                                                           CustomerDiquRatio.city_id == None,
                                                           ))
            if q2.count() == 1:
                t = q2.one()
                qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
            else:
                q3 = DBSession.query(City).filter(and_(City.active == 0, City.id == city_id))
                if q3.count() == 1:
                    t = q3.one()
                    qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
                else:
                    q4 = DBSession.query(Province).filter(and_(Province.active == 0, Province.id == province_id))
                    if q4.count() == 1:
                        t = q4.one()
                        qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio

#        try:
#            t = DBSession.query(CustomerDiquRatio).filter(and_(CustomerDiquRatio.active == 0,
#                                                           CustomerDiquRatio.customer_id == customer_id,
#                                                           CustomerDiquRatio.province_id == province_id,
#                                                           CustomerDiquRatio.city_id == city_id,
#                                                           )).one()
#            qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
#        except:
#            try:
#                t = DBSession.query(CustomerDiquRatio).filter(and_(CustomerDiquRatio.active == 0,
#                                                           CustomerDiquRatio.customer_id == customer_id,
#                                                           CustomerDiquRatio.province_id == province_id,
#                                                           CustomerDiquRatio.city_id == None,
#                                                           )).one()
#                qty_ratio, weight_ratio, vol_ratio = t.qty_ratio, t.weight_ratio, t.vol_ratio
#            except:
#                try:
#                    c = DBSession.query(City).filter(and_(City.active == 0, City.id == city_id)).one()
#                    qty_ratio, weight_ratio, vol_ratio = c.qty_ratio, c.weight_ratio, c.vol_ratio
#                except:
#                    try:
#                        p = DBSession.query(Province).filter(and_(Province.active == 0, Province.id == province_id)).one()
#                        qty_ratio, weight_ratio, vol_ratio = p.qty_ratio, p.weight_ratio, p.vol_ratio
#                    except: pass

        return {'qty_ratio' : qty_ratio, 'weight_ratio' : weight_ratio, 'vol_ratio' : vol_ratio}



    def ajax_order_info(self):
        ref_no = _g('order_no')
        try:
            header = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderHeader.ref_no == ref_no)).one()
            logs = []
            logs.extend(header.get_logs())
            try:
                deliver_detail = DBSession.query(DeliverDetail).filter(and_(DeliverDetail.active == 0, DeliverDetail.order_header_id == header.id)).one()
                deliver_heaer = deliver_detail.header
                logs.extend(deliver_heaer.get_logs())
            except:
                pass
            logs = sorted(logs, cmp = lambda x, y: cmp(x.transfer_date, y.transfer_date))

            return jsonify({'code' : 0 , 'msg' : '', 'data' : {
                                                               'no' : header.no,
                                                               'ref_no' :header.ref_no,
                                                               'status' : header.status,
                                                               'source_company' : unicode(header.source_company),
                                                               'source_province' : unicode(header.source_province),
                                                               'source_city' : unicode(header.source_city) or '',
                                                               'source_address' : header.source_address or '',
                                                               'source_contact' : header.source_contact or '',
															   'source_tel' : header.source_tel or '',
                                                               'destination_company' : unicode(header.destination_company),
                                                               'destination_province' : unicode(header.destination_province),
                                                               'destination_city' : unicode(header.destination_city) or '',
                                                               'destination_address' : header.destination_address or '',
                                                               'destination_contact' : header.destination_contact or '',
															   'destination_tel' : header.destination_tel or '',
															   'qty' : header.qty or '',
															   'weight' : header.weight or '',
                                                               'create_time' : date2text(header.create_time),
															   'expect_time' : header.expect_time or '',
                                                               'actual_time' : header.actual_time or '',
															   'signed_contact' : header.signed_contact or '',
                                                               'logs' : [{
                                                                          'transfer_date' : l.transfer_date,
                                                                          'remark' : l.remark,
                                                                          } for l in logs]
                                                               }})

        except:
            _error(traceback.print_exc())
            return jsonify({'code' : 1, 'msg' : MSG_RECORD_NOT_EXIST})


bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
