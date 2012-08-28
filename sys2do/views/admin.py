# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-13
#  @author: cl.lam
#  Description:
###########################################
'''
import traceback
from datetime import datetime as dt
from flask import Blueprint, render_template, url_for, request, session
from flask.views import View
from flask.helpers import flash, jsonify
from werkzeug.utils import redirect
from webhelpers import paginate
from sqlalchemy.sql.expression import desc, and_
import json

from sys2do.setting import PAGINATE_PER_PAGE
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.views import BasicView
from sys2do.model import DBSession
from sys2do.model.auth import User, Group, Permission
from sys2do.constant import MESSAGE_ERROR, MSG_NO_SUCH_ACTION, \
    MSG_NO_ID_SUPPLIED, MSG_RECORD_NOT_EXIST, MESSAGE_INFO, MSG_SAVE_SUCC, \
    MSG_UPDATE_SUCC, MSG_DELETE_SUCC, MSG_SERVER_ERROR
from sys2do.util.common import _g, _gl, getMasterAll, _error, _gp, _info
from sys2do.model.master import Customer, CustomerProfile, \
    SupplierProfile, Supplier, Payment, Item, PickupType, PackType, Ratio, \
    Receiver, InventoryLocation, CustomerTarget, Note, CustomerContact, \
    Barcode, Province, City, CustomerDiquRatio
from sys2do.util.barcode_helper import generate_barcode_file

__all__ = ['bpAdmin']

bpAdmin = Blueprint('bpAdmin', __name__)

class AdminView(BasicView):

#    decorators = [login_required, ]

    @tab_highlight('TAB_MASTER')
    @templated('admin/index.html')
    def index(self):
        return {}

    @tab_highlight('TAB_DASHBOARD')
    def user(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            page = _g('page') or 1
            objs = DBSession.query(User).filter(User.active == 0).order_by(User.name).all()
            def url_for_page(**params): return url_for('bpAdmin.view', action = 'user', m = 'LIST', page = params['page'])
            records = paginate.Page(objs, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template('admin/user_index.html', records = records)
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


    @tab_highlight('TAB_DASHBOARD')
    def group(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            page = _g('page') or 1
            objs = DBSession.query(Group).filter(Group.active == 0).order_by(Group.name).all()
            def url_for_page(**params): return url_for('bpAdmin.view', action = 'group', m = 'LIST', page = params['page'])
            records = paginate.Page(objs, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template('admin/group_index.html', records = records)

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



    @tab_highlight('TAB_DASHBOARD')
    def permission(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            page = _g('page') or 1
            objs = DBSession.query(Permission).filter(Permission.active == 0).order_by(Permission.name).all()
            def url_for_page(**params): return url_for('bpAdmin.view', action = 'permission', m = 'LIST', page = params['page'])
            records = paginate.Page(objs, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template('admin/permission_index.html', records = records)
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
            DBSession.commit()
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



    @tab_highlight('TAB_MASTER')
    def supplier(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            if _g('SEARCH_SUBMIT'):  # come from search
                values = {'page' : 1}
                for f in ['no', 'name', 'contact_person', 'phone', 'mobile', ] :
                    values[f] = _g(f)
                values['field'] = _g('field', None) or 'create_time'
                values['direction'] = _g('direction', None) or 'desc'
            else: #come from paginate or return
                values = session.get('master_supplier_values', {})
                if _g('page') : values['page'] = int(_g('page'))
                elif 'page' not in values : values['page'] = 1

            session['master_supplier_values'] = values

            conditions = [Supplier.active == 0]
            if values.get('no', None):  conditions.append(Supplier.no.op('like')('%%%s%%' % values['no']))
            if values.get('name', None):  conditions.append(Supplier.name.op('like')('%%%s%%' % values['name']))
            if values.get('contact_person', None):  conditions.append(Supplier.contact_person.op('like')('%%%s%%' % values['contact_person']))
            if values.get('phone', None):  conditions.append(Supplier.phone.op('like')('%%%s%%' % values['phone']))
            if values.get('mobile', None):  conditions.append(Supplier.mobile.op('like')('%%%s%%' % values['mobile']))

            field = values.get('field', 'create_time')
            if values.get('direction', 'desc') == 'desc':
                result = DBSession.query(Supplier).filter(and_(*conditions)).order_by(desc(getattr(Supplier, field)))
            else:
                result = DBSession.query(Supplier).filter(and_(*conditions)).order_by(getattr(Supplier, field))
            def url_for_page(**params): return url_for('bpAdmin.view', action = 'supplier', m = 'LIST', page = params['page'])
            records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

            return render_template('admin/supplier_index.html', records = records, values = values)

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

            try:
                obj = DBSession.query(Supplier).get(id)
                fields = ['no', 'name', 'address', 'phone', 'mobile', 'contact_person', 'remark', 'email', 'payment_id']
                old_info = obj.serialize(fields)

                if not obj :
                    flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                    return redirect(url_for('.view', action = 'supplier'))
                for f in fields:
                    setattr(obj, f, _g(f))
                DBSession.commit()

                #handle the system log
                new_info = obj.serialize(fields)
                change_result = obj.compare(old_info, new_info)
                obj.insert_system_logs(change_result)


                flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
                return redirect(url_for('.view', action = 'supplier'))
            except:
                _error(traceback.print_exc())
                DBSession.rollback()
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
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



    def _template(self, DBObj, action,
                  index_page = 'admin/template_index.html',
                  new_page = 'admin/template_new.html',
                  update_page = 'admin/template_update.html',
                  ):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'LIST':
            page = _g('page') or 1
            objs = DBSession.query(DBObj).filter(DBObj.active == 0).order_by(DBObj.name)
            def url_for_page(**params): return url_for('bpAdmin.view', action = action, m = 'LIST', page = params['page'])
            records = paginate.Page(objs, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template(index_page, records = records, action = action)
        elif method == 'NEW':
            return render_template(new_page, action = action)
        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = action))
            obj = DBSession.query(DBObj).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = action))
            return render_template(update_page, v = obj.populate(), action = action, obj = obj)

        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = action))
            obj = DBSession.query(DBObj).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = action))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = action))
        elif method == 'SAVE_NEW':
            try:
                obj = DBObj.saveAsNew(request.values)
                DBSession.commit()
                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            except:
                _error(traceback.print_exc())
                DBSession.rollback()
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = action))
        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = action))
            obj = DBSession.query(DBObj).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = action))
            try:
                old_info = obj.serialize(obj._get_fields())
                obj.saveAsUpdate(request.values)
                DBSession.commit()

                new_info = obj.serialize(obj._get_fields())
                change_result = obj.compare(old_info, new_info)
                obj.insert_system_logs(change_result)
                flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            except:
                _error(traceback.print_exc())
                DBSession.rollback()
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = action))


    @tab_highlight('TAB_MASTER')
    def item(self):
        return self._template(Item, 'item')

    @tab_highlight('TAB_MASTER')
    def payment(self):
        return self._template(Payment, 'payment')

    @tab_highlight('TAB_MASTER')
    def pickuptype(self):
        return self._template(PickupType, 'pickuptype')

    @tab_highlight('TAB_MASTER')
    def packtype(self):
        return self._template(PackType, 'packtype')


    @tab_highlight('TAB_MASTER')
    def ratio(self):
        method = _g('m', 'LIST')
        if method not in ['UPDATE', 'SAVE_UPDATE']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))
        if method == 'UPDATE':
            ratios = {}
            for r in DBSession.query(Ratio).filter(Ratio.active == 0):
                ratios[r.type] = r.value
            return render_template('admin/ratio.html', ratios = ratios)
        elif method == 'SAVE_UPDATE':
            for r in DBSession.query(Ratio).filter(Ratio.active == 0):
                if r.type in request.values:
                    r.value = _g(r.type) or 0
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('bpAdmin.view'))


    @tab_highlight('TAB_MASTER')
    def receiver(self):
        return self._template(Receiver, 'receiver',
                              index_page = 'admin/receiver_index.html',
                              new_page = 'admin/receiver_new.html',
                              update_page = 'admin/receiver_update.html',)


    @tab_highlight('TAB_MASTER')
    def note(self):
        return self._template(Note, 'note',
                              index_page = 'admin/note_index.html',
                              new_page = 'admin/note_new.html',
                              update_page = 'admin/note_update.html',)







    @tab_highlight('TAB_MASTER')
    def diqu(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE', 'ADD_CITY', 'DELETE_CITY']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))

        if method == 'LIST':
            page = _g('page') or 1
            objs = DBSession.query(Province).filter(Province.active == 0).order_by(Province.name).all()
            def url_for_page(**params): return url_for('bpAdmin.view', action = 'diqu', m = 'LIST', page = params['page'])
            records = paginate.Page(objs, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template('admin/diqu_index.html', records = records)
        elif method == 'NEW':
            return render_template('admin/diqu_new.html')

        elif method == 'UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'customer'))
            obj = DBSession.query(Province).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'diqu'))

            city_json = [{
                          'id' : 'old_%s' % c.id,
                          'city_name' : c.name,
                          'city_code' : c.code,
                          'city_shixiao' : c.shixiao,
                          } for c in obj.children()]

            return render_template('admin/diqu_update.html', obj = obj, city_json = json.dumps(city_json))

        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'diqu'))
            obj = DBSession.query(Province).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'diqu'))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'diqu'))

        elif method == 'SAVE_NEW':
            obj = Province(name = _g('name'), code = _g('code'), shixiao = _g('shixiao'))
            DBSession.add(obj)

            city_json = _g('city_json', '')
            for city in json.loads(city_json):
                DBSession.add(City(
                                   name = city.get('city_name', None),
                                   code = city.get('city_code', None),
                                   shixiao = city.get('city_shixiao', None),
                                   parent_code = obj.code
                                   ))
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'diqu'))


        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'diqu'))
            obj = DBSession.query(Province).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = 'diqu'))

            for f in ['name', 'code', 'shixiao']:
                setattr(obj, f, _g(f))

            city_json = _g('city_json', '')
            city_ids = map(lambda v : v.id, obj.children())
            for city in json.loads(city_json):
                if not city.get('id', None) : continue
                if isinstance(city['id'], basestring) and city['id'].startswith("old_"):  #existing target
                    cid = city['id'].split("_")[1]
                    c = DBSession.query(City).get(cid)
                    c.name = city.get('city_name', None)
                    c.code = city.get('city_code', None)
                    c.shixiao = city.get('city_shixiao', None)
                    c.parent_code = obj.code
                    city_ids.remove(c.id)
                else:
                    DBSession.add(City(
                                       name = city.get('city_name', None),
                                       code = city.get('city_code', None),
                                       shixiao = city.get('city_shixiao', None),
                                       parent_code = obj.code
                                       ))

            DBSession.query(City).filter(City.id.in_(city_ids)).update({'active' : 1}, False)
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'diqu'))
        elif method == 'ADD_CITY':
            try:
                city = City(name = _g('city_name'), code = _g('city_code'), parent_code = _g('code'), shixiao = _g('city_shixiao'))
                DBSession.add(city)
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : MSG_SAVE_SUCC , 'data' : city.populate()})
            except:
                _error(traceback.print_exc())
                DBSession.rollback()
                return jsonify({'code' : 1, 'msg' : MSG_SERVER_ERROR})
        elif method == 'DELETE_CITY':
            id = _g('id', None)
            if not id : return jsonify({'code' : 1, 'msg' : MSG_NO_ID_SUPPLIED})
            try:
                obj = DBSession.query(City).get(id)
                obj.active = 1
                DBSession.commit()
                return jsonify({'code' : 0 , 'msg' : MSG_DELETE_SUCC})
            except:
                _error(traceback.print_exc())
                DBSession.rollback()
                return jsonify({'code' : 1, 'msg' : MSG_SERVER_ERROR})


    @tab_highlight('TAB_MASTER')
    def barcode(self):
        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'PRINT', 'SAVE_NEW']:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
            return redirect(url_for('.view', action = 'index'))

        DBObj = Barcode
        index_page = 'admin/barcode_index.html'
        new_page = 'admin/barcode_new.html'
        print_page = 'admin/barcode_print.html'
        action = 'barcode'

        if method == 'LIST':
            if _g('SEARCH_SUBMIT'):  # come from search
                values = {'page' : 1}
                for f in ['value', 'ref_no', 'status', 'create_time_from', 'create_time_to'] :
                    values[f] = _g(f)
                values['field'] = _g('field', None) or 'create_time'
                values['direction'] = _g('direction', None) or 'desc'
            else: #come from paginate or return
                values = session.get('master_barcode_values', {})
                if _g('page') : values['page'] = int(_g('page'))
                elif 'page' not in values : values['page'] = 1

            session['master_barcode_values'] = values

            conditions = [DBObj.active == 0]
            if values.get('value', None):  conditions.append(DBObj.value.op('like')('%%%s%%' % values['value']))
            if values.get('ref_no', None):  conditions.append(DBObj.ref_no.op('like')('%%%s%%' % values['ref_no']))
            if values.get('status', None):  conditions.append(DBObj.status == values['status'])
            if values.get('create_time_from', None):  conditions.append(DBObj.create_time > values['create_time_from'])
            if values.get('create_time_to', None):    conditions.append(DBObj.create_time < '%s 23:59' % values['create_time_to'])

            field = values.get('field', 'create_time')
            if values.get('direction', 'desc') == 'desc':
                result = DBSession.query(DBObj).filter(and_(*conditions)).order_by(desc(getattr(DBObj, field)))
            else:
                result = DBSession.query(DBObj).filter(and_(*conditions)).order_by(getattr(DBObj, field))

            def url_for_page(**params): return url_for('bpAdmin.view', action = action, m = 'LIST', page = params['page'])
            records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = 100, url = url_for_page)
            return render_template(index_page, records = records, action = action, values = values)

        elif method == 'NEW':
            return render_template(new_page, action = action)
        elif method == 'PRINT':
            ids = _gl('ids')
            records = DBSession.query(DBObj).filter(DBObj.id.in_(ids)).order_by(desc(DBObj.create_time))
            return render_template(print_page, records = records)
        elif method == 'SAVE_NEW':
            qty = _g('qty')
            records = [DBObj.getOrCreate(None, None, status = 1) for i in range(int(qty))]
            DBSession.commit()
            if _g('type') == 'CREATE':
                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
                return redirect(url_for('.view', action = action))
            else:
                return render_template(print_page, records = records)
#    def warehouse(self, DBObj, action,
#                  index_page = 'admin/template_index.html',
#                  new_page = 'admin/template_new.html',
#                  update_page = 'admin/template_update.html',
#                  ):
#        
#        DBObj = InventoryLocation
#        action = 'warehouse'
#        
#        
#        method = _g('m', 'LIST')
#        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE']:
#            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR);
#            return redirect(url_for('.view', action = 'index'))
#        if method == 'LIST':
#            result = {}
#            for line in DBSession.query(DBObj).filter(DBObj.active == 0):
#                if not line.parent_id:
#                    
#            
#            
#            
#            return render_template(index_page, records = objs, action = action)
#        elif method == 'NEW':
#            return render_template(new_page, action = action)
#        elif method == 'UPDATE':
#            id = _g('id', None)
#            if not id :
#                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
#                return redirect(url_for('.view', action = action))
#            obj = DBSession.query(DBObj).get(id)
#            if not obj :
#                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
#                return redirect(url_for('.view', action = action))
#            return render_template(update_page, v = obj.populate(), action = action)
#
#        elif method == 'DELETE':
#            id = _g('id', None)
#            if not id :
#                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
#                return redirect(url_for('.view', action = action))
#            obj = DBSession.query(DBObj).get(id)
#            if not obj :
#                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
#                return redirect(url_for('.view', action = action))
#            obj.active = 1
#            DBSession.commit()
#            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
#            return redirect(url_for('.view', action = action))
#        elif method == 'SAVE_NEW':
#            try:
#                obj = DBObj.saveAsNew(request.values)
#                DBSession.commit()
#                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
#            except:
#                _error(traceback.print_exc())
#                DBSession.rollback()
#                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
#            return redirect(url_for('.view', action = action))
#        elif method == 'SAVE_UPDATE':
#            id = _g('id', None)
#            if not id :
#                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
#                return redirect(url_for('.view', action = 'user'))
#            obj = DBSession.query(DBObj).get(id)
#            if not obj :
#                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
#                return redirect(url_for('.view', action = 'user'))
#            try:
#                obj.saveAsUpdate(request.values)
#                DBSession.commit()
#                flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
#            except:
#                DBSession.rollback()
#                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
#            return redirect(url_for('.view', action = action))




bpAdmin.add_url_rule('/', view_func = AdminView.as_view('view'), defaults = {'action':'index'})
bpAdmin.add_url_rule('/<action>', view_func = AdminView.as_view('view'))
