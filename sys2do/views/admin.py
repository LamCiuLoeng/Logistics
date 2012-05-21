# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-13
#  @author: cl.lam
#  Description:
###########################################
'''
from flask import Blueprint, render_template, url_for, request
from flask.views import View
from flask.helpers import flash
from werkzeug.utils import redirect

from sys2do.util.decorator import templated
from sys2do.views import BasicView
from sys2do.model import DBSession
from sys2do.model.auth import User, Group, Permission
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_NO_ID_SUPPLIED, MSG_RECORD_NOT_EXIST, MESSAGE_INFO, MSG_SAVE_SUCC, \
    MSG_UPDATE_SUCC
from sys2do.util.common import _g, _gl

__all__ = ['bpAdmin']

bpAdmin = Blueprint('bpAdmin', __name__)

class AdminView(BasicView):

    @templated('admin/index.html')
    def index(self):
        return {}


    def user(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            users = DBSession.query(User).filter(User.active == 0).order_by(User.name).all()
            return render_template('admin/user_index.html', records = users)
        elif method == 'NEW':
            groups = Group.all()
            return render_template('admin/user_new.html', groups = groups)
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            user = User.get(id)
            if not user :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            gids = map(lambda v:v.id, user.groups)
            all_groups = Group.all()
            return render_template('admin/user_update.html', v = user.populate(), gids = gids, all_groups = all_groups)
        elif method == 'DELETE':
            pass
        elif method == 'SAVE_NEW':
            user = User.saveAsNew(request.values)
            gids = _gl('gids')
            user.groups = DBSession.query(Group).filter(Group.id.in_(gids)).all()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'user'))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            user = User.get(id)
            if not user :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            user.saveAsUpdate(request.values)
            user.groups = DBSession.query(Group).filter(Group.id.in_(_gl('gids'))).all()
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'user'))


    def group(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            groups = DBSession.query(Group).filter(Group.active == 0).order_by(Group.name).all()
            return render_template('admin/group_index.html', records = groups)
        elif method == 'NEW':
            return render_template('admin/group_new.html', users = User.all(), permissions = Permission.all())
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            group = Group.get(id)
            if not group :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            return render_template('admin/group_update.html',
                                   v = group.populate(),
                                   uids = map(lambda v:v.id, group.users),
                                   all_users = User.all(),
                                   pids = map(lambda v:v.id, group.permissions),
                                   all_permissions = Permission.all())
        elif method == 'DELETE':
            pass
        elif method == 'SAVE_NEW':
            group = Group.saveAsNew(request.values)
            group.users = DBSession.query(User).filter(User.id.in_(_gl("uids"))).all()
            group.permissions = DBSession.query(Permission).filter(Permission.id.in_(_gl("pids"))).all()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'group'))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            group = Group.get(id)
            if not group :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            group.saveAsUpdate(request.values)
            group.users = DBSession.query(User).filter(User.id.in_(_gl("uids"))).all()
            group.permissions = DBSession.query(Permission).filter(Permission.id.in_(_gl("pids"))).all()
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'group'))


    def permission(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            permission = DBSession.query(Permission).filter(Permission.active == 0).order_by(Permission.name).all()
            return render_template('admin/permission_index.html', records = permission)
        elif method == 'NEW':
            groups = Group.all()
            return render_template('admin/permission_new.html', groups = groups)
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            permission = Permission.get(id)
            if not permission :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            gids = map(lambda v:v.id, permission.groups)
            all_groups = Group.all()
            return render_template('admin/permission_update.html', v = permission.populate(), gids = gids, all_groups = all_groups)
        elif method == 'DELETE':
            pass
        elif method == 'SAVE_NEW':
            permission = Permission.saveAsNew(request.values)
            permission.groups = DBSession.query(Group).filter(Group.id.in_(_gl("gids"))).all()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'permission'))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            permission = Permission.get(id)
            if not permission :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            permission.saveAsUpdate(request.values)
            permission.groups = DBSession.query(Group).filter(Group.id.in_(_gl('gids'))).all()
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'permission'))


bpAdmin.add_url_rule('/', view_func = AdminView.as_view('view'), defaults = {'action':'index'})
bpAdmin.add_url_rule('/<action>', view_func = AdminView.as_view('view'))
