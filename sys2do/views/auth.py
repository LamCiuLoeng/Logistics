# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-5
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt
from flask import session
from flask.helpers import url_for, flash
from werkzeug.utils import redirect
from flask.blueprints import Blueprint
from flaskext.babel import gettext as _
from sqlalchemy.sql.expression import and_


from sys2do.util.decorator import templated
from sys2do.util.common import _g, getMasterAll
from sys2do.model import DBSession, User
from sys2do.constant import MESSAGE_ERROR, MSG_USER_NOT_EXIST, \
    MSG_WRONG_PASSWORD, MESSAGE_INFO, MSG_SAVE_SUCC
from sys2do.model.master import Customer, CustomerProfile
from sys2do.util.tests import in_group


__all__ = ['bpAuth']



index_url = lambda : url_for('bpRoot.view', action = "index")



bpAuth = Blueprint('bpAuth', __name__)

@bpAuth.route('/login')
@templated("login.html")
def login():
    if session.get('login', None):
        return redirect(index_url())
    return {}



@bpAuth.route('/check', methods = ['GET', 'POST'])
def check():
    try:
        u = DBSession.query(User).filter(and_(User.active == 0, User.name == _g('name'))).one()
    except:
        flash(MSG_USER_NOT_EXIST, MESSAGE_ERROR)
        return redirect(url_for('bpAuth.login', next = _g('next')))
    else:
        if not u.validate_password(_g('password')):
            flash(MSG_WRONG_PASSWORD, MESSAGE_ERROR)
            return redirect(url_for('bpAuth.login', next = _g('next')))
        else:
            #fill the info into the session
            session['login'] = True
            session['user_profile'] = u.populate()
            permissions = set()
            for g in u.groups:
                for p in g.permissions:
                    permissions.add(p.name)
            session['user_profile']['groups'] = [g.name for g in u.groups]
            session['user_profile']['permissions'] = list(permissions)

            if in_group('CUSTOMER'):
                for g in u.groups:
                    if g.type != 0 :
                        for p in g.customer_profile:
                            if p and p.customer_id:
                                session['customer_profile'] = p.customer.populate()
                                break

            if in_group('SUPPLIER'):
                for g in u.groups:
                    if g.type != 0 :
                        for p in g.supplier_profile:
                            if p and p.supplier_id:
                                session['supplier_profile'] = p.supplier.populate()
                                break

            u.last_login = dt.now()

            session.permanent = True

            DBSession.commit()
            if _g('next') : return redirect(_g('next'))
            return redirect(index_url())


@bpAuth.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('user_profile', None)
    if 'customer_profile' in session : session.pop('customer_profile', None)
    if 'supplier_profile' in session : session.pop('supplier_profile', None)
    return redirect(url_for('bpAuth.login'))


@bpAuth.route('/register')
@templated("register.html")
def register():
    return {'customers' : getMasterAll(Customer), }



@bpAuth.route('/save_register', methods = ['GET', 'POST'])
def save_register():
    cid = _g('customer_id' , None)
    user_params = {
                "name" : _g('name'),
                "password" : _g('password'),
                "email" : _g('email'),
                "first_name" : _g('first_name'),
                "last_name" : _g('last_name'),
                "phone" : _g('phone'),
                "mobile" : _g('mobile'),
                   }


    if cid and cid != 'OTHER':
        c = DBSession.query(Customer).get(cid)
        user_params['customer_profile_id'] = c.profile.id
    else:
        cname = _g('name').strip()
        cp = CustomerProfile(name = "PROFILE_%s" % cname.strip().upper().replace(' ', '_'))
        DBSession.add(cp)
        DBSession.flush()
        c = Customer(
                     name = cname,
                     address = _g('address'),
                     profile = cp
                     )
        user_params['customer_profile_id'] = cp.id
        DBSession.add(c)

    DBSession.add(User(**user_params))

    DBSession.commit()
    flash(MSG_SAVE_SUCC, MESSAGE_INFO)
    return redirect(url_for('bpAuth.login'))
