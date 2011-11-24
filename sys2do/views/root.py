# -*- coding: utf-8 -*-
import traceback
import os
from datetime import datetime as dt
from flask import g, render_template, flash, session, redirect, url_for, request
from flaskext.babel import gettext as _
from sqlalchemy import and_

from sys2do import app
from sys2do.model import DBSession, User
from flask.helpers import jsonify
from sys2do.util.decorator import templated, login_required, has_all_permissions
from sys2do.util.common import _g, MESSAGE_ERROR, MESSAGE_INFO, upload
from sys2do.setting import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_URL

from sys2do.views.base import createHandler, Handler



@templated("index.html")
def index():
#    flash('hello!', MESSAGE_INFO)
#    flash('SHIT!', MESSAGE_ERROR)
    app.logger.debug('A value for debugging')
    return {"content" : _("Hello,World!")}




@templated("login.html")
def _login():
    if session.get('login', None):
        return redirect(url_for("index"))
    return {}


def _check():
    try:
        u = DBSession.query(User).filter(and_(User.active == 0, User.name == _g('name'))).one()
    except:
        flash(_('This user does not exist!'))
        return redirect(url_for('authHandler'))
    else:
        if u.password != _g('password'):
            flash(_('The password is wrong!'))
            return redirect('%s?action=login' % url_for('authHandler'))
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
        return redirect(url_for('index'))



def _logout():
    session.pop('login', None)
    session.pop('user_profile', None)
    return redirect(url_for('authHandler'))


authHandler = createHandler(User,
                      name_for_url = 'authHandler',
                      default_action = 'login',
                      redirect_url = '/auth',
                      action_mapping = {'login' : _login, 'check' : _check, 'logout' : _logout}
                      )

