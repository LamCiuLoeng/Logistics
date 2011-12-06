# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-28
#  @author: cl.lam
#  Description:
###########################################
'''


from flask import Blueprint

from flask.views import View
from werkzeug.utils import redirect
from flask.helpers import url_for, flash
from sys2do.model.logic import OrderHeader
from sys2do.model import DBSession
from sys2do.util.decorator import templated, login_required
from sys2do import app
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_UPDATE_SUCC, \
    MSG_DELETE_SUCC, MSG_NO_ID_SUPPLIED, MSG_SERVER_ERROR, MSG_NO_SUCH_ACTION
from sys2do.util.common import _g, getOr404


__all__ = ['bpOrder']

bpOrder = Blueprint('bpOrder', __name__)

class OrderView(View):
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


    @templated('order/index.html')
    def index(self):
        result = DBSession.query(OrderHeader).filter(OrderHeader.active == 0)
        return {'result' : result }

    @templated('order/add.html')
    def add(self):
        return {}

    def save_new(self):
        params = {}
        for f in ['no', 'source_company']:
            params[f] = _g(f) or None
        header = DBSession.add(OrderHeader(**params))
        DBSession.commit()
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))

    @templated('order/update.html')
    def revise(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)
        values = header.populate()
        return {'values' : values }


    def save_update(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)

        fields = ['no', 'source_company', ]
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

    def cancel(self):
        id = _g('id') or None
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())

        header = DBSession.query(OrderHeader).get(id)
        header.active = 1
        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view', action = 'index'))

    @templated('order/received.html')
    def received(self):
        header = getOr404(OrderHeader, _g('id'), self.default())
        return {'values' : header.populate()}

    def received_save(self):
        header = getOr404(OrderHeader, _g('id'), self.default())
        header.target_company = _g('target_company') or None
        DBSession.commit()
        flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
        return redirect(self.default())


bpOrder.add_url_rule('/', view_func = OrderView.as_view('view'), defaults = {'action':'index'})
bpOrder.add_url_rule('/<action>', view_func = OrderView.as_view('view'))

