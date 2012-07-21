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
from sqlalchemy.sql.expression import and_
from flask.blueprints import Blueprint
from flask.helpers import flash, jsonify

from sys2do.views import BasicView
from sys2do.util.decorator import templated, login_required
from sys2do.model.master import Customer, CustomerTarget
from sys2do.model import DBSession
from sys2do.util.common import _g, getMasterAll, _error
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC, MSG_UPDATE_SUCC, \
    MSG_SERVER_ERROR
from sys2do.model.logic import OrderHeader




__all__ = ['bpFin']

bpFin = Blueprint('bpFin', __name__)

class FinView(BasicView):

    decorators = [login_required]

    @templated('fin/index.html')
    def index(self):
        values = {}
        for f in ['no', 'create_time_from', 'create_time_to', 'ref_no', 'source_station',
                  'source_company_id', 'destination_station', 'destination_company_id'] :
            values[f] = _g(f)

        if not values['create_time_from'] and not values['create_time_to']:
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")


        conditions = [OrderHeader.active == 0]
        if values['create_time_from']:
            conditions.append(OrderHeader.create_time > values['create_time_from'])
        if values['create_time_to']:
            conditions.append(OrderHeader.create_time < '%s 23:59' % values['create_time_to'])
        if values['ref_no']:
            conditions.append(OrderHeader.ref_no.op('like')('%%%s%%' % values['ref_no']))
        if values['no']:
            conditions.append(OrderHeader.no.op('like')('%%%s%%' % values['no']))
        if values['source_station']:
            conditions.append(OrderHeader.source_station.op('like')('%%%s%%' % values['source_station']))
        if values['source_company_id']:
            conditions.append(OrderHeader.source_company_id == values['source_company_id'])
            targets = DBSession.query(CustomerTarget).filter(and_(CustomerTarget.active == 0, CustomerTarget.customer_id == values['source_company_id']))
        else:
            targets = []

        if values['destination_station']:
            conditions.append(OrderHeader.destination_station.op('like')('%%%s%%' % values['destination_station']))
        if values['destination_company_id']:
            conditions.append(OrderHeader.destination_company_id == values['destination_company_id'])

        result = DBSession.query(OrderHeader).filter(and_(*conditions)).order_by(OrderHeader.create_time.desc())

        total_qty = total_vol = total_weight = total_amount = 0
        for r in result:
            if r.qty : total_qty += r.qty
            if r.vol : total_vol += r.vol
            if r.weight : total_weight += r.weight
            if r.amount : total_amount += r.amount

        return {'result' : result ,
                'values' : values ,
                'total_qty' : total_qty ,
                'total_vol' : total_vol,
                'total_weight' : total_weight,
                'total_amount' : total_amount,
                'customers' : getMasterAll(Customer),
                'targets' : targets,
                }



    def ajax_change_flag(self):
        try:
            ids = _g('order_ids', '').split("|")
            flag = _g('flag')
            type = _g('type')
            for r in DBSession.query(OrderHeader).filter(OrderHeader.id.in_(ids)).order_by(OrderHeader.create_time):
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


bpFin.add_url_rule('/', view_func = FinView.as_view('view'), defaults = {'action':'index'})
bpFin.add_url_rule('/<action>', view_func = FinView.as_view('view'))
