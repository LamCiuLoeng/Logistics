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

from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.views import BasicView
from sys2do.model import DBSession
from sys2do.model.auth import User, Group, Permission
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_NO_ID_SUPPLIED, MSG_RECORD_NOT_EXIST, MESSAGE_INFO, MSG_SAVE_SUCC, \
    MSG_UPDATE_SUCC, MSG_DELETE_SUCC
from sys2do.util.common import _g, _gl, getMasterAll
from sys2do.model.master import Customer, CustomerProfile, \
    SupplierProfile, Supplier, Payment

__all__ = ['bpAdmin']

bpAdmin = Blueprint('bpAdmin', __name__)

class AdminView(BasicView):

    decorators = [login_required, ]

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
            obj = User.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            gids = map(lambda v:v.id, obj.groups)
            all_groups = Group.all()
            return render_template('admin/user_update.html', v = obj.populate(), gids = gids, all_groups = all_groups)
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            obj = User.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            obj.active = 1
            obj.group = []
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'user'))
        elif method == 'SAVE_NEW':
            obj = User.saveAsNew(request.values)
            gids = _gl('gids')
            obj.groups = DBSession.query(Group).filter(Group.id.in_(gids)).all()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'user'))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            obj = User.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'user'))
            obj.saveAsUpdate(request.values)
            obj.groups = DBSession.query(Group).filter(Group.id.in_(_gl('gids'))).all()
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
            obj = Group.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            return render_template('admin/group_update.html',
                                   v = obj.populate(),
                                   uids = map(lambda v:v.id, obj.users),
                                   all_users = User.all(),
                                   pids = map(lambda v:v.id, obj.permissions),
                                   all_permissions = Permission.all())
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            obj = Group.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            obj.active = 1
            obj.users = []
            obj.permissions = []
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'group'))
        elif method == 'SAVE_NEW':
            obj = Group.saveAsNew(request.values)
            obj.users = DBSession.query(User).filter(User.id.in_(_gl("uids"))).all()
            obj.permissions = DBSession.query(Permission).filter(Permission.id.in_(_gl("pids"))).all()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'group'))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            obj = Group.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'group'))
            obj.saveAsUpdate(request.values)
            obj.users = DBSession.query(User).filter(User.id.in_(_gl("uids"))).all()
            obj.permissions = DBSession.query(Permission).filter(Permission.id.in_(_gl("pids"))).all()
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'group'))


    def permission(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            permissions = DBSession.query(Permission).filter(Permission.active == 0).order_by(Permission.name).all()
            return render_template('admin/permission_index.html', records = permissions)
        elif method == 'NEW':
            groups = Group.all()
            return render_template('admin/permission_new.html', groups = groups)
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            obj = Permission.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            gids = map(lambda v:v.id, obj.groups)
            all_groups = Group.all()
            return render_template('admin/permission_update.html', v = obj.populate(), gids = gids, all_groups = all_groups)
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            obj = Permission.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            obj.active = 1
            obj.groups = []
            obj.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'permission'))
        elif method == 'SAVE_NEW':
            obj = Permission.saveAsNew(request.values)
            obj.groups = DBSession.query(Group).filter(Group.id.in_(_gl("gids"))).all()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'permission'))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            obj = Permission.get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'permission'))
            obj.saveAsUpdate(request.values)
            obj.groups = DBSession.query(Group).filter(Group.id.in_(_gl('gids'))).all()
            obj.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'permission'))


    @tab_highlight('TAB_CUSTOMER')
    def customer(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            customers = DBSession.query(Customer).filter(Customer.active == 0).order_by(Customer.name).all()
            return render_template('admin/customer_index.html', records = customers)
        elif method == 'NEW':
            return render_template('admin/customer_new.html', payment = getMasterAll(Payment))
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            obj = DBSession.query(Customer).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            return render_template('admin/customer_update.html', obj = obj , payment = getMasterAll(Payment))
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            obj = DBSession.query(Customer).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'customer'))
        elif method == 'SAVE_NEW':
            obj = Customer(
                                no = _g('no'),
                                name = _g('name'),
                                address = _g('address'),
                                phone = _g('phone'),
                                mobile = _g('mobile'),
                                contact_person = _g('contact_person'),
                                email = _g('email'),
                                payment_id = _g('payment_id'),
                                remark = _g('remark')
                                )
            DBSession.add(obj)
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'customer'))

        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            obj = DBSession.query(Customer).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            for f in ['no', 'name', 'address', 'phone', 'contact_person', 'remark', 'email', 'payment_id', 'mobile', ]:
                setattr(obj, f, _g(f))
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'customer'))



    def cprofile(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'cprofile'))
        if method == 'LIST':
            cps = DBSession.query(CustomerProfile).filter(CustomerProfile.active == 0).order_by(CustomerProfile.name).all()
            return render_template('admin/customer_profile_index.html', records = cps)
        elif method == 'NEW':
            customers = DBSession.query(Customer).filter(Customer.active == 0).order_by(Customer.name).all()
            groups = DBSession.query(Group).filter(Group.active == 0).order_by(Group.name).all()
            return render_template('admin/customer_profile_new.html', customers = customers, groups = groups)
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'cprofile'))
            obj = DBSession.query(CustomerProfile).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'cprofile'))
            return render_template('admin/customer_profile_update.html', obj = obj)
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'cprofile'))
            obj = DBSession.query(CustomerProfile).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'cprofile'))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'cprofile'))
        elif method == 'SAVE_NEW':
            obj = CustomerProfile(
                                name = _g('name'),
                                remark = _g('remark'),
                                customer_id = _g('customer_id'),
                                group_id = _g('group_id')
                                )
            DBSession.add(obj)
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'cprofile'))

        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'cprofile'))
            obj = DBSession.query(CustomerProfile).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'cprofile'))
            for f in ['name', 'remark', 'customer_id', 'group_id']:
                setattr(obj, f, _g(f))
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'cprofile'))



    @tab_highlight('TAB_SUPPLIER')
    def supplier(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            suppliers = DBSession.query(Supplier).filter(Supplier.active == 0).order_by(Supplier.name).all()
            return render_template('admin/supplier_index.html', records = suppliers)
        elif method == 'NEW':
            return render_template('admin/supplier_new.html', payment = getMasterAll(Payment))

        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'supplier'))
            obj = DBSession.query(Supplier).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'supplier'))
            return render_template('admin/supplier_update.html', obj = obj, payment = getMasterAll(Payment))
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'supplier'))
            obj = DBSession.query(Supplier).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'supplier'))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'supplier'))
        elif method == 'SAVE_NEW':
            obj = Supplier(
                                no = _g('no'),
                                name = _g('name'),
                                address = _g('address'),
                                phone = _g('phone'),
                                mobile = _g('mobile'),
                                email = _g('email'),
                                contact_person = _g('contact_person'),
                                remark = _g('remark'),
                                payment_id = _g('payment_id'),
                                )
            DBSession.add(obj)
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'supplier'))

        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'supplier'))
            obj = DBSession.query(Supplier).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'supplier'))
            for f in ['no', 'name', 'address', 'phone', 'mobile', 'contact_person', 'remark', 'email', 'payment_id']:
                setattr(obj, f, _g(f))
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'supplier'))





    def sprofile(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'cprofile'))
        if method == 'LIST':
            cps = DBSession.query(SupplierProfile).filter(SupplierProfile.active == 0).order_by(SupplierProfile.name).all()
            return render_template('admin/supplier_profile_index.html', records = cps)
        elif method == 'NEW':
            suppliers = DBSession.query(Supplier).filter(Supplier.active == 0).order_by(Supplier.name).all()
            groups = DBSession.query(Group).filter(Group.active == 0).order_by(Group.name).all()
            return render_template('admin/supplier_profile_new.html', suppliers = suppliers, groups = groups)
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'sprofile'))
            obj = DBSession.query(SupplierProfile).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'sprofile'))
            suppliers = DBSession.query(Supplier).filter(Supplier.active == 0).order_by(Supplier.name).all()
            groups = DBSession.query(Group).filter(Group.active == 0).order_by(Group.name).all()
            return render_template('admin/supplier_profile_update.html', suppliers = suppliers, groups = groups, obj = obj)
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'sprofile'))
            obj = DBSession.query(SupplierProfile).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'sprofile'))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'sprofile'))
        elif method == 'SAVE_NEW':
            obj = SupplierProfile(
                                name = _g('name'),
                                remark = _g('remark'),
                                customer_id = _g('customer_id'),
                                group_id = _g('group_id')
                                )
            DBSession.add(obj)
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'sprofile'))

        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'sprofile'))
            obj = DBSession.query(SupplierProfile).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'sprofile'))
            for f in ['name', 'remark', 'supplier_id', 'group_id']:
                setattr(obj, f, _g(f))
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'sprofile'))

bpAdmin.add_url_rule('/', view_func = AdminView.as_view('view'), defaults = {'action':'index'})
bpAdmin.add_url_rule('/<action>', view_func = AdminView.as_view('view'))
