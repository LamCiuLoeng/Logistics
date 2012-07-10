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
from sys2do.util.decorator import templated, login_required
from sys2do.util.common import _g, _gp, _gl
from sys2do.constant import MESSAGE_ERROR, MESSAGE_INFO, MSG_NO_SUCH_ACTION, \
    MSG_SAVE_SUCC
from sys2do.views import BasicView
from sys2do.model.master import CustomerProfile, Customer
from sys2do.model.logic import OrderHeader
from sys2do.util.logic_helper import genSystemNo


__all__ = ['bpRoot']

bpRoot = Blueprint('bpRoot', __name__)


class RootView(BasicView):

    @login_required
    @templated("index.html")
    def index(self):
    #    flash('hello!', MESSAGE_INFO)
    #    flash('SHIT!', MESSAGE_ERROR)
#        app.logger.debug('A value for debugging')
#        flash(TEST_MSG, MESSAGE_INFO)
#        return send_file('d:/new.png', as_attachment = True)
        return {"content" : _("Hello,World!")}


    def ajax_master(self):
        master = _g('m')
        if master == 'customer':
            cs = DBSession.query(Customer).filter(Customer.active == 0).order_by(Customer.name).all()
            return jsonify({'status' : 0, 'msg' : '', 'data' : cs})
        elif master == 'city':
            pid = _g('pid')
            cs = DBSession.query(City).filter(and_(City.active == 0, City.province_id == pid)).all()
            return jsonify({'status' : 0, 'msg' : '', 'data' : [{'id' : c.id , 'name' : unicode(c)} for c in cs]})
        elif master == 'district':
            cid = _g('cid')
            ds = DBSession.query(District).filter(and_(District.active == 0, District.city_id == cid)).all()
            return jsonify({'status' : 0, 'msg' : '', 'data' : [{'id' : d.id , 'name' : unicode(d)} for d in ds]})
        return jsonify({'status' : 1, 'msg' : 'Error', })


bpRoot.add_url_rule('/', view_func = RootView.as_view('view'), defaults = {'action':'index'})
bpRoot.add_url_rule('/<action>', view_func = RootView.as_view('view'))
