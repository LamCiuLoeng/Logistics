# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
from datetime import datetime as dt, timedelta
import traceback
import json
from werkzeug.utils import redirect
from sqlalchemy.sql.expression import and_, desc
from flask.blueprints import Blueprint
from flask.helpers import flash, jsonify, url_for
from flask import session
from webhelpers import paginate
from flask.templating import render_template
from flask.globals import request

from sys2do.views import BasicView
from sys2do.util.decorator import templated, login_required, tab_highlight
from sys2do.model.master import Customer, CustomerTarget, Province, \
    CustomerSource, CustomerContact, CustomerDiquRatio
from sys2do.model import DBSession
from sys2do.util.common import _g, getMasterAll, _error, _info, upload, \
    multiupload, _gp
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC, MSG_UPDATE_SUCC, \
    MSG_SERVER_ERROR, MESSAGE_ERROR, MSG_NO_ID_SUPPLIED, MSG_DELETE_SUCC, MSG_RECORD_NOT_EXIST, \
    MSG_NO_SUCH_ACTION
from sys2do.model.logic import OrderHeader
from sys2do.setting import PAGINATE_PER_PAGE
from sys2do.model.system import SystemLog






__all__ = ['bpCustomer']

bpCustomer = Blueprint('bpCustomer', __name__)

class CustomerView(BasicView):

    decorators = [login_required]


    @tab_highlight('TAB_MASTER')
    def index(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['no', 'name', 'contact_person', 'phone', 'mobile', 'province_id', 'city_id'] :
                values[f] = _g(f)
            values['field'] = _g('field', None) or 'create_time'
            values['direction'] = _g('direction', None) or 'desc'
        else: #come from paginate or return
            values = session.get('master_customer_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1

        session['master_customer_values'] = values

        conditions = [Customer.active == 0]
        if values.get('no', None):  conditions.append(Customer.no.op('like')('%%%s%%' % values['no']))
        if values.get('name', None):  conditions.append(Customer.name.op('like')('%%%s%%' % values['name']))
        if values.get('contact_person', None):  conditions.append(Customer.contact_person.op('like')('%%%s%%' % values['contact_person']))
        if values.get('phone', None):  conditions.append(Customer.phone.op('like')('%%%s%%' % values['phone']))
        if values.get('mobile', None):  conditions.append(Customer.mobile.op('like')('%%%s%%' % values['mobile']))
        if values.get('province_id', None):
            conditions.append(Customer.province_id == values['province_id'])
            sp = DBSession.query(Province).get(values['province_id'])
            cites = sp.children()
        else: cites = []
        if values.get('city_id', None): conditions.append(Customer.city_id == values['city_id'])


        # for the sort function
        field = values.get('field', 'create_time')
        if values.get('direction', 'desc') == 'desc':
            result = DBSession.query(Customer).filter(and_(*conditions)).order_by(desc(getattr(Customer, field)))
        else:
            result = DBSession.query(Customer).filter(and_(*conditions)).order_by(getattr(Customer, field))
#            objs = DBSession.query(Customer).filter(Customer.active == 0).order_by(Customer.name).all()
        def url_for_page(**params): return url_for('bpAdmin.view', action = 'customer', m = 'LIST', page = params['page'])

        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
        return render_template('customer/customer_index.html',
                               records = records,
                               values = values , cites = cites,)


    @templated('customer/customer_view.html')
    def view(self):
        id = _g('id')
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        obj = DBSession.query(Customer).get(id)
        return {'obj' : obj}




    @templated('customer/customer_new.html')
    def add(self):
        return {}

    def save_new(self):
        try:
            obj = Customer(
                            no = _g('no'),
                            name = _g('name'),
                            display_name = _g('display_name'),
                            province_id = _g('province_id'),
                            city_id = _g('city_id'),
                            address = _g('address'),
                            contact_person = _g('contact_person'),
                            mobile = _g('mobile'),
                            phone = _g('phone'),
                            email = _g('email'),
                            remark = _g('remark'),
                            note_id = _g('note_id'),
#                            payment_id = _g('payment_id'),
                                )
            DBSession.add(obj)
            obj.attachment = multiupload()
            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = 'view', id = obj.id))
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view'))



    @templated('customer/customer_update.html')
    def update(self):
        id = _g('id')
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        obj = DBSession.query(Customer).get(id)
        if obj.province_id :
            cities = obj.province.children()
        else:
            cities = []
        return {'obj' : obj, 'cities' : cities}


    def save_update(self):
        id = _g('id', None)
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        obj = DBSession.query(Customer).get(id)
        if not obj :
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        try:
            fields = ['no', 'name', 'display_name', 'province_id', 'city_id',
                      'address', 'contact_person', 'mobile', 'phone', 'email', 'note_id', 'remark']
            old_info = obj.serialize(fields) # to used for the history log
            for f in fields:
                setattr(obj, f, _g(f))

            #handle the file upload
            old_attachment_ids = map(lambda (k, v) : v, _gp("old_attachment_"))
            old_attachment_ids.extend(multiupload())
            obj.attachment = old_attachment_ids

            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
#            return redirect(url_for('.view',id=obj.id))
            new_info = obj.serialize(fields)
            change_result = obj.compare(old_info, new_info)
            obj.insert_system_logs(change_result)
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for('.view', action = "view", id = obj.id))


    def delete(self):
        id = _g('id', None)
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        obj = DBSession.query(Customer).get(id)
        if not obj :
            flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
            return redirect(url_for('.view'))
        obj.active = 1
        DBSession.commit()
        flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        return redirect(url_for('.view'))


    def source(self):
        DBObj = CustomerSource
        _action = "source"
        _fields = ['name', 'province_id', 'city_id', 'remark', 'payment_id']
        _contact_type = 'S'
        _index_html = 'customer/customer_source_index.html'
        _new_html = 'customer/customer_source_new.html'
        _update_html = 'customer/customer_source_update.html'
        return self._subcompany(DBObj, _action, _fields, _contact_type, _index_html, _new_html, _update_html)


    def target(self):
        DBObj = CustomerTarget
        _action = "target"
        _fields = ['name', 'province_id', 'city_id', 'remark', ]
        _contact_type = 'T'
        _index_html = 'customer/customer_target_index.html'
        _new_html = 'customer/customer_target_new.html'
        _update_html = 'customer/customer_target_update.html'
        return self._subcompany(DBObj, _action, _fields, _contact_type, _index_html, _new_html, _update_html)


    def _subcompany(self, DBObj, _action, _fields, _contact_type, _index_html, _new_html, _update_html):
#        DBObj = CustomerSource
#        _action = "source"
#        _fields = ['name', 'province_id', 'city_id', 'remark', 'payment_id']
#        _contact_type = 'S'
#        _index_html = 'customer/customer_source_index.html'
#        _new_html = 'customer/customer_source_new.html'
#        _update_html = 'customer/customer_source_update.html'

        method = _g('m', 'LIST')
        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE', ]:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'index'))

        if method == 'LIST':
            id = _g('id')
            c = DBSession.query(Customer).get(id)
            result = DBSession.query(DBObj).filter(and_(DBObj.active == 0,
                                                        DBObj.customer_id == c.id)).order_by(DBObj.name)

            page = _g('page', 1)
            def url_for_page(**params): return url_for('.view', action = _action, m = 'LIST', page = params['page'], id = id)
            records = paginate.Page(result, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template(_index_html, records = records, customer = c)
        elif method == 'NEW':
            customer_id = _g('customer_id')
            return render_template(_new_html, customer_id = customer_id)
        elif method == 'SAVE_NEW':
            try:
                params = {"customer_id" : _g('customer_id')}
                for f in _fields : params[f] = _g(f)
                obj = DBObj(**params)
                DBSession.add(obj)
                DBSession.flush()
                contact_json = _g('contact_json', '')
                for contact in json.loads(contact_json):
                    DBSession.add(CustomerContact(
                                                  customer_id = _g('customer_id'),
                                                  type = _contact_type,
                                                  refer_id = obj.id,
                                                  name = contact['contact_name'],
                                                  address = contact['contact_address'],
                                                  mobile = contact['contact_mobile'],
                                                  phone = contact['contact_phone'],
                                                  remark = contact['contact_remark'],
                                                  ))
                DBSession.commit()
                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            except:
                DBSession.rollback()
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = _action, id = obj.customer_id))

        elif method == 'UPDATE':
            source = DBSession.query(DBObj).get(_g('id'))
            if source.province_id:
                cities = source.province.children()
            else:
                cities = []
            contact_json = []
            for c in source.contacts():
                contact_json.append({
                                    "id" : "old_%s" % c.id,
                                    "contact_name" : c.name,
                                    "contact_address" : c.address,
                                    "contact_phone" : c.phone,
                                    "contact_mobile" : c.mobile,
                                    "contact_remark" : c.remark,
                                    })
            return render_template(_update_html, cities = cities,
                                   obj = source, contact_json = json.dumps(contact_json))

        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            obj = DBSession.query(DBObj).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))

            for f in _fields : setattr(obj, f, _g(f))
            contact_ids = [c.id for c in obj.contacts()]
            contact_json = _g('contact_json', '')
            for c in json.loads(contact_json):
                if not c.get('id', None) : continue
                if isinstance(c['id'], basestring) and c['id'].startswith("old_"):  #existing contact
                    cid = c['id'].split("_")[1]
                    t = DBSession.query(CustomerContact).get(cid)
                    t.name = c.get('contact_name', None)
                    t.address = c.get('contact_address', None)
                    t.mobile = c.get('contact_mobile', None)
                    t.phone = c.get('contact_phone', None)
                    t.remark = c.get('contact_remark', None)
                    contact_ids.remove(t.id)
                else:
                    DBSession.add(CustomerContact(
                                                customer_id = obj.customer_id,
                                                type = _contact_type,
                                                refer_id = obj.id,
                                                name = c.get('contact_name', None),
                                                address = c.get('contact_address', None),
                                                mobile = c.get('contact_mobile', None),
                                                phone = c.get('contact_phone', None),
                                                email = c.get('contact_email', None),
                                                remark = c.get('contact_remark', None),
                                                  ))

            DBSession.query(CustomerContact).filter(CustomerContact.id.in_(contact_ids)).update({'active' : 1}, False)
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = _action, id = obj.customer_id))
        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            obj = DBSession.query(DBObj).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            DBSession.query(DBObj).filter(DBObj.id == id).update({'active' : 1}, False)
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = _action))


    def pricelist(self):
        method = _g('m', 'LIST')
        _action = 'pricelist'

        if method not in ['LIST', 'NEW', 'UPDATE', 'DELETE', 'SAVE_NEW', 'SAVE_UPDATE', ]:
            flash(MSG_NO_SUCH_ACTION, MESSAGE_ERROR)
            return redirect(url_for('.view', action = 'index'))

        if method == 'LIST':
            id = _g('id')
            c = DBSession.query(Customer).get(id)
            result = DBSession.query(CustomerDiquRatio).filter(and_(CustomerDiquRatio.active == 0,
                                                                    CustomerDiquRatio.customer_id == c.id,
                                                        )).order_by(CustomerDiquRatio.province_id)

            page = _g('page', 1)
            def url_for_page(**params): return url_for('.view', action = _action, m = 'LIST', page = params['page'], id = id)
            records = paginate.Page(result, page, show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)
            return render_template("customer/customer_pricelist_index.html", records = records, customer = c)

        elif method == 'NEW':
            customer_id = _g('customer_id')
            return render_template("customer/customer_pricelist_new.html", customer_id = customer_id)
        elif method == 'SAVE_NEW':
            try:
                params = {}
                for f in ['customer_id', 'province_id', 'city_id', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'remark'] :
                    params[f] = _g(f)
                obj = CustomerDiquRatio(**params)
                DBSession.add(obj)
                DBSession.commit()
                flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            except:
                DBSession.rollback()
                flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for('.view', action = _action, id = obj.customer_id))
        elif method == 'UPDATE':
            obj = DBSession.query(CustomerDiquRatio).get(_g('id'))
            if obj.province_id:
                cities = obj.province.children()
            else:
                cities = []
            return render_template("customer/customer_pricelist_update.html", cities = cities, obj = obj)

        elif method == 'SAVE_UPDATE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            obj = DBSession.query(CustomerDiquRatio).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            for f in ['province_id', 'city_id', 'qty_ratio', 'weight_ratio', 'vol_ratio', 'remark'] :
                setattr(obj, f, _g(f))
            DBSession.commit()
            flash(MSG_UPDATE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = _action, id = obj.customer_id))

        elif method == 'DELETE':
            id = _g('id', None)
            if not id :
                flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            obj = DBSession.query(CustomerDiquRatio).get(id)
            if not obj :
                flash(MSG_RECORD_NOT_EXIST, MESSAGE_ERROR)
                return redirect(url_for('.view', action = _action))
            obj.active = 1
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = _action))




bpCustomer.add_url_rule('/', view_func = CustomerView.as_view('view'), defaults = {'action':'index'})
bpCustomer.add_url_rule('/<action>', view_func = CustomerView.as_view('view'))
