# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-6
#  @author: cl.lam
#  Description:
###########################################
'''
from flask.blueprints import Blueprint
from flask.views import View
from flask.helpers import url_for, flash
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION, MESSAGE_INFO, \
    MSG_SAVE_SUCC
from werkzeug.utils import redirect
from sys2do.util.decorator import templated
from sys2do.model import DBSession
from sys2do.model.logic import DeliverHeader, OrderHeader
from sqlalchemy.sql.expression import and_
from sys2do.util.common import _gl, _g


__all__ = ['bpDeliver']


bpDeliver = Blueprint('bpDeliver', __name__)

class DeliverView(View):
    methods = ['GET', 'POST']
#    decorators = [login_required]

    def default(self):  return url_for('.view', action = 'index')

    def dispatch_request(self, action):
        return getattr(self, action)()
        try:
            pass
        except AttributeError, e:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(self.default())

    @templated('deliver/index.html')
    def index(self):
        result = DBSession.query(DeliverHeader).filter(DeliverHeader.active == 0)
        return {'result' : result}

    @templated('deliver/add.html')
    def add(self):
        result = DBSession.query(OrderHeader).filter(and_(OrderHeader.active == 0, OrderHeader.status == 0))
        return {'result' : result}



    #===========================================================================
    # error here
    #===========================================================================
    @templated('deliver/add_deliver.html')
    def add_deliver(self):
        ids = _gl('order_ids')
        orders = DBSession.query(DeliverHeader).filter(and_(OrderHeader.active == 0, OrderHeader.id.in_(ids)))
        return {'orders' : orders, 'ids' : ids}



    def deliver_save_new(self):
        header = DeliverHeader(no = _g('no'))
        DBSession.add(header)

        for id in _g('order_ids').split(',') : DBSession.query(OrderHeader).filter(OrderHeader.id == id).status = 1


        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(self.default())


bpDeliver.add_url_rule('/', view_func = DeliverView.as_view('view'), defaults = {'action':'index'})
bpDeliver.add_url_rule('/<action>', view_func = DeliverView.as_view('view'))

