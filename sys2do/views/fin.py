# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
import os
import random
import shutil
from datetime import datetime as dt, timedelta
import traceback
from werkzeug.utils import redirect
from sqlalchemy.sql.expression import and_, desc, select
from flask.blueprints import Blueprint
from flask.helpers import flash, jsonify, url_for, send_file
from flask import session
from webhelpers import paginate


from sys2do.views import BasicView
from sys2do.util.decorator import templated, login_required
from sys2do.model.master import Customer, CustomerTarget, Province, \
    CustomerSource, Supplier
from sys2do.model import DBSession
from sys2do.util.common import _g, getMasterAll, _error, _info
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC, MSG_UPDATE_SUCC, \
    MSG_SERVER_ERROR, SYSTEM_DATE_FORMAT, MSG_NO_ID_SUPPLIED, \
    MSG_RECORD_NOT_EXIST
from sys2do.model.logic import OrderHeader, DeliverHeader, DeliverDetail
from sys2do.setting import PAGINATE_PER_PAGE, TMP_FOLDER, TEMPLATE_FOLDER
from sys2do.model.system import SystemLog
from sys2do.util.excel_helper import ProfitReport




__all__ = ['bpFin']

bpFin = Blueprint('bpFin', __name__)

class FinView(BasicView):

#    decorators = [login_required]

    @templated('fin/index.html')
    def index(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['no', 'create_time_from', 'create_time_to', 'ref_no', 'customer_id', 'source_company_id',
                      'source_province_id', 'source_city_id', 'destination_province_id', 'destination_city_id',
                      'approve', 'paid', 'is_exception', 'is_less_qty', 'is_return_note'] :
                values[f] = _g(f)
                values['field'] = _g('field', None) or 'create_time'
                values['direction'] = _g('direction', None) or 'desc'
        else: #come from paginate or return
            values = session.get('fin_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1


        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['fin_values'] = values


        conditions = [OrderHeader.active == 0]
        if values.get('create_time_from', None):       conditions.append(OrderHeader.order_time > values['create_time_from'])
        if values.get('create_time_to', None):         conditions.append(OrderHeader.order_time < '%s 23:59' % values['create_time_to'])
        if values.get('ref_no', None):                 conditions.append(OrderHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values.get('no', None):                     conditions.append(OrderHeader.no.op('like')('%%%s%%' % values['no']))
        if values.get('source_province_id', None):
            conditions.append(OrderHeader.source_province_id == values['source_province_id'])
            sp = DBSession.query(Province).get(values['source_province_id'])
            source_cites = sp.children()
        else: source_cites = []
        if values.get('source_city_id', None):          conditions.append(OrderHeader.source_city_id == values['source_city_id'])
        if values.get('destination_province_id', None):
            conditions.append(OrderHeader.destination_province_id == values['destination_province_id'])
            dp = DBSession.query(Province).get(values['destination_province_id'])
            destination_cites = dp.children()
        else: destination_cites = []
        if values.get('destination_city_id', None):  conditions.append(OrderHeader.destination_city_id == values['destination_city_id'])

        if values.get('customer_id', None):
            conditions.append(OrderHeader.customer_id == values['customer_id'])
            sources = DBSession.query(CustomerSource).filter(and_(CustomerSource.active == 0, CustomerSource.customer_id == values['customer_id']))
        else:
            sources = []

        if values.get('source_company_id', None):       conditions.append(OrderHeader.source_company_id == values['source_company_id'])
        if values.get('approve', None):        conditions.append(OrderHeader.approve == values['approve'])
        if values.get('paid', None):           conditions.append(OrderHeader.paid == values['paid'])
        if values.get('is_exception', None):   conditions.append(OrderHeader.is_exception == values['is_exception'])
        if values.get('is_less_qty', None):    conditions.append(OrderHeader.is_less_qty == values['is_less_qty'])
        if values.get('is_return_note', None): conditions.append(OrderHeader.is_return_note == values['is_return_note'])

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
                'customers' : getMasterAll(Customer),
                'sources' : sources,
                'records' : records,
                'source_cites' : source_cites,
                'destination_cites' : destination_cites,
                }



    def ajax_change_flag(self):
        try:
            ids = _g('order_ids', '').split("|")
            flag = _g('flag')
            type = _g('type')
            for r in DBSession.query(OrderHeader).filter(OrderHeader.id.in_(ids)).order_by(OrderHeader.create_time):
                if type == 'APPROVE':
                    r.approve = flag
                    if flag == '1':  #approve
                        remark = u'%s 审核通过该订单。' % session['user_profile']['name']
                    else: #disapprove
                        remark = u'%s 审核不通过该订单。' % session['user_profile']['name']
                elif type == 'PAID':
                    r.paid = flag
                    if flag == '1':
                        remark = u'%s 确认该订单为客户已付款。' % session['user_profile']['name']
                    else:
                        remark = u'%s 确认该订单为客户未付款。' % session['user_profile']['name']
                elif type == 'SUPLLIER_PAID':
                    r.supplier_paid = flag
                    if flag == '1':
                        remark = u'%s 确认该订单为已付款予承运商。' % session['user_profile']['name']
                    else:
                        remark = u'%s 确认该订单为未付款予承运商。' % session['user_profile']['name']
                elif type == 'ORDER_RETURN':
                    r.is_return_note = flag
                    if flag == '1':
                        remark = u'%s 确认该订单为客户已返回单。' % session['user_profile']['name']
                    else:
                        remark = u'%s 确认该订单为客户未返回单。' % session['user_profile']['name']
                elif type == 'EXCEPTION':
                    r.is_exception = flag
                    if flag == '1':
                        remark = u'%s 标记该订单为异常。' % session['user_profile']['name']
                    else:
                        remark = u'%s 取消该订单的异常标记。' % session['user_profile']['name']
                elif type == 'LESS_QTY':
                    r.is_less_qty = flag
                    if flag == '1':
                        remark = u'%s 标记该订单为少货。' % session['user_profile']['name']
                    else:
                        remark = u'%s 取消该订单的少货标记。' % session['user_profile']['name']


            DBSession.add(SystemLog(
                                    type = r.__class__.__name__,
                                    ref_id = r.id,
                                    remark = remark
                                    ))
            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : MSG_UPDATE_SUCC})
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            return jsonify({'code' : 1, 'msg' : MSG_SERVER_ERROR})


    @templated('fin/report.html')
    def report(self):
        return {}



    def export(self):
        values = {}
        for f in ['create_time_from', 'create_time_to', 'ref_no',
                  'customer_id', 'source_company_id',
                  'destination_province_id', 'destination_city_id',
                  'supplier_id', 'deliver_header_no',
                  ] :
            values[f] = _g(f)
        conditions = [OrderHeader.active == 0, ]
        if values.get('create_time_from', None):       conditions.append(OrderHeader.order_time > values['create_time_from'])
        if values.get('create_time_to', None):         conditions.append(OrderHeader.order_time < '%s 23:59' % values['create_time_to'])
        if values.get('ref_no', None):                 conditions.append(OrderHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values.get('customer_id', None):            conditions.append(OrderHeader.customer_id == values['customer_id'])
        if values.get('source_company_id', None):            conditions.append(OrderHeader.source_company_id == values['source_company_id'])
        if values.get('destination_province_id', None):            conditions.append(OrderHeader.destination_province_id == values['destination_province_id'])
        if values.get('destination_city_id', None):            conditions.append(OrderHeader.destination_city_id == values['destination_city_id'])
        if values.get('deliver_header_no', None):            conditions.append(OrderHeader.deliver_header_no.op('like')('%%%s%%' % values['destination_city_id']))

        data = []
        index = 1
        total_qty = total_weight = total_amount = total_cost = 0

        subq_condictions = [DeliverHeader.active == 0, DeliverDetail.active == 0, Supplier.active == 0,
                            DeliverHeader.id == DeliverDetail.header_id, DeliverHeader.supplier_id == Supplier.id, ]
        if values.get('supplier_id', None):            subq_condictions.append(DeliverHeader.supplier_id == values['supplier_id'])
        subq = select([Supplier.name, DeliverHeader.no, DeliverDetail.order_header_id]).where(and_(*subq_condictions)).alias()

        q = DBSession.query(OrderHeader, subq.c.name, subq.c.no).outerjoin((subq, subq.c.order_header_id == OrderHeader.id)).filter(and_(*conditions)).order_by(OrderHeader.create_time)
        for (oheader, sname, sno) in q:
            row = [
                   index, oheader.create_time.strftime(SYSTEM_DATE_FORMAT), oheader.customer, oheader.source_company, oheader.ref_no,
                   unicode(oheader.destination_province) + unicode(oheader.destination_city or '') , oheader.qty or '', oheader.weight or '',
                   oheader.amount, sname or '', sno or '',
                   ]
            if oheader.cost:
                if oheader.amount:
                    row.extend([oheader.cost, (oheader.amount - oheader.cost), "%.2f%%" % (oheader.cost * 100 / oheader.amount), "%.2f%%" % (100 - oheader.cost * 100 / oheader.amount), ])
                else:
                    row.extend(['', '', '', ''])
            else:
                row.extend(['', '', '', ''])

            data.append(map(lambda v : unicode(v), row))
            index += 1
            total_qty += oheader.qty or 0
            total_weight += oheader.weight or 0
            total_amount += oheader.amount or 0
            if oheader.cost : total_cost += oheader.cost

        if total_amount:
            data.append([
                    u'合计', '', '', '', '', '', total_qty, total_weight, total_amount, '', '', total_cost, (total_amount - total_cost),
                    "%.2f%%" % (total_cost * 100 / total_amount), "%.2f%%" % (100 - total_cost * 100 / total_amount),
                   ])
        else:
            data.append([
                    u'合计', '', '', '', '', '', 0, 0, 0, '', '', total_cost, (total_amount - total_cost), "", "",
                   ])

        if not os.path.exists(TMP_FOLDER): os.makedirs(TMP_FOLDER)
        current = dt.now()
        templatePath = os.path.join(TEMPLATE_FOLDER, "profit_template.xls")
        tempFileName = os.path.join(TMP_FOLDER, "report_tmp_%s_%d.xls" % (current.strftime("%Y%m%d%H%M%S"), random.randint(0, 1000)))
        realFileName = os.path.join(TMP_FOLDER, "profit_report_%s.xls" % (dt.now().strftime("%Y%m%d%H%M%S")))
        shutil.copy(templatePath, tempFileName)
        report_xls = ProfitReport(templatePath = tempFileName, destinationPath = realFileName)

        report_xls.inputData(data = data)
        report_xls.outputData()
        try:
            os.remove(tempFileName)
        except:
            pass
        return send_file(realFileName, as_attachment = True)



    @templated('fin/profit.html')
    def profit(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in [
                      'no', 'create_time_from', 'create_time_to', 'destination_province_id', 'destination_city_id',
                      'ref_no', 'deliver_no', 'supplier_id', 'payment_id', 'is_discount_return'
                      ] :
                values[f] = _g(f)
                values['field'] = _g('field', None) or 'create_time'
                values['direction'] = _g('direction', None) or 'desc'
        else: #come from paginate or return
            values = session.get('fin_profit_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1


        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['fin_profit_values'] = values


        conditions = [OrderHeader.active == 0,
                      DeliverHeader.active == 0 , DeliverDetail.active == 0, DeliverHeader.id == DeliverDetail.header_id,
                      OrderHeader.id == DeliverDetail.order_header_id,
                      ]
        if values.get('create_time_from', None):       conditions.append(OrderHeader.order_time > values['create_time_from'])
        if values.get('create_time_to', None):         conditions.append(OrderHeader.order_time < '%s 23:59' % values['create_time_to'])
        if values.get('ref_no', None):                 conditions.append(OrderHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values.get('deliver_no', None):             conditions.append(DeliverHeader.no.op('like')('%%%s%%' % values['deliver_no']))
        if values.get('destination_province_id', None):
            conditions.append(OrderHeader.destination_province_id == values['destination_province_id'])
            dp = DBSession.query(Province).get(values['destination_province_id'])
            destination_cites = dp.children()
        else: destination_cites = []
        if values.get('destination_city_id', None):  conditions.append(OrderHeader.destination_city_id == values['destination_city_id'])
        if values.get('supplier_id', None):          conditions.append(DeliverHeader.supplier_id == values['supplier_id'])
        if values.get('payment_id', None):           conditions.append(OrderHeader.payment_id == values['payment_id'])
        if values.get('is_discount_return', None):        conditions.append(OrderHeader.is_discount_return == values['is_discount_return'])

        # for the sort function
        field = values.get('field', 'create_time')
        if values.get('direction', 'desc') == 'desc':
            result = DBSession.query(OrderHeader, DeliverHeader).filter(and_(*conditions))
        else:
            result = DBSession.query(OrderHeader, DeliverHeader).filter(and_(*conditions))

        def url_for_page(**params): return url_for('bpFin.view', action = "profit", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        return {
                'values' : values ,
                'records' : records,
                'destination_cites' : destination_cites,
                }



    def ajax_save_discount(self):
        id = _g('id')
        if not id:
            return jsonify({'code' : 1 , 'msg' : MSG_NO_ID_SUPPLIED})
        header = DBSession.query(OrderHeader).get(id)
        if not header:
            return jsonify({'code' : 1 , 'msg' : MSG_RECORD_NOT_EXIST})

        try:
            for f in ['discount_return_time', 'discount_return_person_id', 'discount_return_remark', 'actual_proxy_charge']:
                setattr(header, f, _g(f))
            header.is_discount_return = 1
            DBSession.commit()
            return jsonify({'code' : 0 , 'msg' : MSG_SAVE_SUCC})
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            return jsonify({'code' : 1 , 'msg' : MSG_SERVER_ERROR})


    def ajax_get_discount(self):
        id = _g('id')
        if not id:
            return jsonify({'code' : 1 , 'msg' : MSG_NO_ID_SUPPLIED})
        header = DBSession.query(OrderHeader).get(id)
        if not header:
            return jsonify({'code' : 1 , 'msg' : MSG_RECORD_NOT_EXIST})

        return jsonify({'code' : 0 , 'data' : {
                                             'ref_no' : header.ref_no,
                                             'actual_proxy_charge' : header.actual_proxy_charge,
                                             'discount_return_time' : header.discount_return_time,
                                             'discount_return_person_id' : header.discount_return_person_id,
                                             'discount_return_remark' : header.discount_return_remark,
                                             }})

bpFin.add_url_rule('/', view_func = FinView.as_view('view'), defaults = {'action':'index'})
bpFin.add_url_rule('/<action>', view_func = FinView.as_view('view'))
