# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt, timedelta
import traceback
from werkzeug.utils import redirect
from sqlalchemy.sql.expression import and_, desc
from flask.blueprints import Blueprint
from flask.helpers import flash, jsonify, url_for
from flask import session
from webhelpers import paginate

from sys2do.views import BasicView
from sys2do.util.decorator import templated, login_required
from sys2do.model.master import Customer, CustomerTarget, Province
from sys2do.model import DBSession
from sys2do.util.common import _g, getMasterAll, _error
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC, MSG_UPDATE_SUCC, \
    MSG_SERVER_ERROR
from sys2do.model.logic import OrderHeader
from sys2do.setting import PAGINATE_PER_PAGE
from sys2do.model.system import SystemLog




__all__ = ['bpFin']

bpFin = Blueprint('bpFin', __name__)

class FinView(BasicView):

    decorators = [login_required]

    @templated('fin/index.html')
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
            values = session.get('fin_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1


        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['fin_values'] = values


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
                'customers' : getMasterAll(Customer),
                'targets' : targets,
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


bpFin.add_url_rule('/', view_func = FinView.as_view('view'), defaults = {'action':'index'})
bpFin.add_url_rule('/<action>', view_func = FinView.as_view('view'))
