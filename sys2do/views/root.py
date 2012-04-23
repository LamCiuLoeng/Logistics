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
from flask.helpers import jsonify
from sys2do.util.decorator import templated
from sys2do.util.common import _g, _gp, _gl
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC
from sys2do.views import BasicView
from sys2do.model.master import CustomerProfile, Customer
from sys2do.model.logic import OrderHeader, OrderLog, OrderDetail
from sys2do.util.logic_helper import genSystemNo


__all__ = ['bpRoot']

bpRoot = Blueprint('bpRoot', __name__)


class RootView(BasicView):

    @templated("index.html")
    def index(self):
    #    flash('hello!', MESSAGE_INFO)
    #    flash('SHIT!', MESSAGE_ERROR)
        app.logger.debug('A value for debugging')
        return {"content" : _("Hello,World!")}


    @templated('add.html')
    def add(self):
        cps = DBSession.query(CustomerProfile).all()
        companys = []
        vendors = []
        items = []
        units = []
        for cp in cps:
            companys.extend(cp.customers)
            vendors.extend(cp.vendors)
            items.extend(cp.items)
            units.extend(cp.itemunits)
        return {'companys' :companys , 'vendors' : vendors, 'items' : items, 'units' : units}


    def save(self):
        c = _g('company')
        v = _g('vendor')

        no = genSystemNo()
        order = OrderHeader(no = no, customer_id = c, vendor_id = v)
        DBSession.add(order)

        for (k, v), (uk, uv) in zip(_gp('item_'), _gp('unit_')):
            n, id = k.split("_")
            DBSession.add(OrderDetail(header = order, item_id = id, order_qty = v, item_unit_id = uv))

        DBSession.commit()
        flash(MSG_SAVE_SUCC, MESSAGE_INFO)
        return redirect(url_for('bpRoot.view', action = 'index'))


    @templated('track.html')
    def track(self):
        orders = DBSession.query(OrderHeader).filter(OrderHeader.active == 0).all()
        return {'orders' : orders}


    @templated('search_orders.html')
    def search_orders(self):
        nos = _g('nos')
        logs = []
        for no in nos.split(','):
            log = DBSession.query(OrderLog).filter(and_(OrderHeader.id == OrderLog.order_id, OrderHeader.no == no, OrderLog.active == 0)).all()
            logs.append((no, log))
        return {'logs' : logs}


    def test(self):
        print _gp('aa_')
        return redirect(url_for('bpRoot.view', action = 'index'))


    def ajax_master(self):
        master = _g('m')
        if(master == 'customer'):
            cs = DBSession.query(Customer).filter(Customer.active == 0).order_by(Customer.name).all()
            return jsonify({'status' : 0, 'msg' : '', 'data' : cs})
        return


bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
