# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-12
#  @author: cl.lam
#  Description:
###########################################
'''
from flask.blueprints import Blueprint
from flask.views import View
from flask.helpers import url_for, flash
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION
from werkzeug.utils import redirect
from sys2do.util.common import _g
from sys2do.views import BasicView
from sys2do.model.master import Customer
from sys2do.model import DBSession
from flask.templating import render_template

__all__ = ['bpMaster']

bpMaster = Blueprint('bpMaster', __name__)

class MasterView(BasicView):

    def index(self):
        type = _g('type')
        master_mapping = {
                          'customer' : Customer,
#                          'vendor' : Vendor,
#                          'item' : Item,
                          }

        if type not in master_mapping :
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect('/index')

        clz = master_mapping[type]
        result = DBSession.query(clz).filter(clz.active == 0).order_by(clz.name)
        return render_template('master/%s_index.html' % type, result = result)


    def update(self):
        return ''


bpMaster.add_url_rule('/', view_func = MasterView.as_view('view'), defaults = {'action':'index'})
bpMaster.add_url_rule('/<action>', view_func = MasterView.as_view('view'))
