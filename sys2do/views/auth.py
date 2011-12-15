# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-5
#  @author: cl.lam
#  Description:
###########################################
'''
from flask import session
from flask.helpers import url_for, flash
from werkzeug.utils import redirect
from flask.blueprints import Blueprint
from flaskext.babel import gettext as _
from sqlalchemy.sql.expression import and_


from sys2do.util.decorator import templated
from sys2do.util.common import _g
from sys2do.model import DBSession, User


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
        flash(_('This user does not exist!'))
        return redirect(url_for('bpAuth.login'))
    else:
        if u.password != _g('password'):
            flash(_('The password is wrong!'))
            return redirect(url_for('bpAuth.login'))
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
        return redirect(index_url())


@bpAuth.route('/logout')
def logout():
    session.pop('login', None)
    session.pop('user_profile', None)
    return redirect(index_url())


@bpAuth.route('/register')
@templated("register.html")
def register():
    return {}


@bpAuth.route('/save_register', methods = ['GET', 'POST'])
def save_register():
    return 'OK'
