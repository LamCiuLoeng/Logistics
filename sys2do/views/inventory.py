# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-12-15
#  @author: cl.lam
#  Description:
###########################################
'''
import json
import traceback
from datetime import datetime as dt, timedelta
from flask.helpers import flash, url_for, jsonify
from flask.blueprints import Blueprint
from werkzeug.utils import redirect
from flask import session
from webhelpers import paginate
from sqlalchemy.sql.expression import and_, desc


from sys2do.views import BasicView
from sys2do.util.decorator import templated, login_required
from sys2do.model.master import InventoryLocation, InventoryItem, \
    InventoryInNote, InventoryNoteDetail, InventoryOutNote, \
    InventoryLocationItem
from sys2do.model import DBSession
from sys2do.util.common import _g, _gl, _gp, _error, _info
from sys2do.constant import MESSAGE_INFO, MSG_SAVE_SUCC, MSG_NO_ID_SUPPLIED, \
    MESSAGE_ERROR, MSG_SERVER_ERROR, MSG_DELETE_SUCC

from sys2do.setting import PAGINATE_PER_PAGE
from sys2do.util.logic_helper import getInNoteNo, getOutNo



__all__ = ['bpInventory']

bpInventory = Blueprint('bpInventory', __name__)

class InventoryView(BasicView):

#    decorators = [login_required]

    @templated('inventory/index.html')
    def index(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['item_id', 'location_id', 'children_location' ] :
                values[f] = _g(f)
        else: #come from paginate or return
            values = session.get('inventory_index_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1

        session['inventory_index_values'] = values
        conditions = [InventoryItem.active == 0]

        if values.get('item_id', None):
            conditions.append(InventoryLocationItem.item_id == values['item_id'])
        if values.get('location_id', None):
            if values.get('children_location', None) == 'Y':
                location = DBSession.query(InventoryLocation).get(values['location_id'])
                conditions.extend([
                                   InventoryLocation.active == 0,
                                   InventoryLocation.full_path_ids.like('%s%%' % location.full_path_ids),
                                   InventoryLocation.id == InventoryLocationItem.location_id,
                                   ])
            else:
                conditions.append(InventoryLocationItem.location_id == values['location_id'])
            conditions.append(InventoryLocationItem.location_id == values['location_id'])


        result = DBSession.query(InventoryLocationItem).filter(and_(*conditions)).order_by(InventoryItem.name)
        def url_for_page(**params): return url_for('.view', action = "item_detail", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        root_locations = DBSession.query(InventoryLocation).filter(and_(InventoryLocation.active == 0,
                                                       InventoryLocation.parent_id == None)).order_by(InventoryLocation.name)
        return {
                'values' : values ,
                'records' : records,
                'locations' : root_locations,
                }


    @templated('inventory/item_detail.html')
    def item_detail(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['create_time_from', 'create_time_to', 'id'] :
                values[f] = _g(f)
        else: #come from paginate or return
            values = session.get('inventory_item_detail_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1
            values['id'] = _g('id')

        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['inventory_item_detail_values'] = values

        conditions = [InventoryNoteDetail.active == 0, InventoryNoteDetail.item_id == values.get('id', None)]
        result = DBSession.query(InventoryNoteDetail).filter(and_(*conditions)).order_by(InventoryNoteDetail.create_time)

        def url_for_page(**params): return url_for('.view', action = "item_detail", id = values.get('id', None), page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        return {
                "records" : records,
                "values"  : values,
                }



    @templated('inventory/in_note_index.html')
    def in_note(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['no', 'create_time_from', 'create_time_to', 'customer_id', 'location_id' ] :
                values[f] = _g(f)
                values['field'] = _g('field', None) or 'create_time'
                values['direction'] = _g('direction', None) or 'desc'
        else: #come from paginate or return
            values = session.get('inventory_in_note_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1

        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['inventory_in_note_values'] = values


        conditions = [InventoryInNote.active == 0]
        if values.get('create_time_from', None):       conditions.append(InventoryInNote.create_time > values['create_time_from'])
        if values.get('create_time_to', None):         conditions.append(InventoryInNote.create_time < '%s 23:59' % values['create_time_to'])
        if values.get('no', None):                     conditions.append(InventoryInNote.no.op('like')('%%%s%%' % values['no']))

        if values.get('customer_id', None):
            conditions.append(InventoryInNote.customer_id == values['customer_id'])
        if values.get('location_id', None):
            conditions.extend([
                               InventoryNoteDetail.active == 0,
                               InventoryNoteDetail.type == 'IN',
                               InventoryNoteDetail.header_id == InventoryInNote.id,
                               InventoryNoteDetail.location_id == values['location_id'],
                               ])

        # for the sort function
        field = values.get('field', 'create_time')
        if values.get('direction', 'desc') == 'desc':
            result = DBSession.query(InventoryInNote).filter(and_(*conditions)).order_by(desc(getattr(InventoryInNote, field)))
        else:
            result = DBSession.query(InventoryInNote).filter(and_(*conditions)).order_by(getattr(InventoryInNote, field))

        def url_for_page(**params): return url_for('.view', action = "in_note", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        root_locations = DBSession.query(InventoryLocation).filter(and_(InventoryLocation.active == 0,
                                                       InventoryLocation.parent_id == None)).order_by(InventoryLocation.name)
        return {
                'values' : values ,
                'records' : records,
                'locations' : root_locations,
                }

    @templated('inventory/in_note_review.html')
    def in_note_review(self):
        id = _g('id')
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())
        obj = DBSession.query(InventoryInNote).get(id)
        return {'obj' : obj}


    @templated('inventory/in_note_new.html')
    def in_note_new(self):
        pass


    def in_note_save_new(self):
        params = {
                  "customer_id" : _g('customer_id'),
                  "so" : _g('so'),
                  "po" : _g('po'),
                  "dn" : _g('dn'),
                  "ref" : _g('ref'),
                  "remark" : _g('remark'),
                  }
        try:
            header = InventoryInNote(**params)
            DBSession.add(header)
            DBSession.flush()

            total_qty = total_area = total_weight = 0

            item_json = _g('item_json', '')
            for item in json.loads(item_json):
                if item['item_id']:
                    dbItem = DBSession.query(InventoryItem).get(item['item_id'])
                    try:
                        locationItem = DBSession.query(InventoryLocationItem).filter(and_(
                                                                                InventoryLocationItem.active == 0,
                                                                                InventoryLocationItem.item_id == item['item_id'],
                                                                                InventoryLocationItem.location_id == item['location_id'],
                                                                                )).with_lockmode("update").one()
                    except:
                        locationItem = InventoryLocationItem(item = dbItem, location_id = item['location_id'],)
                else:
                    dbItem = InventoryItem(name = item['item_name'], desc = item['desc'])
                    locationItem = InventoryLocationItem(item = dbItem, location_id = item['location_id'],)
                    DBSession.add_all([dbItem, locationItem])
                    DBSession.flush()


                d = InventoryNoteDetail(header_id = header.id, type = 'IN' , item = dbItem,
                                                      desc = item['desc'], qty = item['qty'] or 0, weight = item['weight'] or 0,
                                                      area = item['area'] or 0, remark = item['remark'],
                                                      location_id = item['location_id'],
                                                      )
                DBSession.add(d)
                if d.qty :
                    total_qty += int(d.qty)
                    locationItem.qty += int(d.qty)
                    locationItem.exp_qty += int(d.qty)
                if d.area :
                    total_area += float(d.area)
                    locationItem.area += float(d.area)
                    locationItem.exp_area += float(d.area)
                if d.weight :
                    total_weight += float(d.weight)
                    locationItem.weight += float(d.weight)
                    locationItem.exp_weight += float(d.weight)

            header.no = getInNoteNo(header.id)
            header.qty = total_qty
            header.weight = total_weight
            header.area = total_area

            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for(".view", action = "in_note_review", id = header.id))
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for(".view", action = "in_note"))

    def in_note_update(self):
        pass




    def in_note_delete(self):
        id = _g(id)
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(url_for(".view", action = "in_note"))
        try:
            note = DBSession.query(InventoryInNote).get(id)
            note.active = 1
            for d in note.details:
                location_item = DBSession.query(InventoryLocationItem).filter(and_(InventoryLocationItem.active == 0,
                                                               InventoryLocationItem.location_id == d.refer_location_id,
                                                               InventoryLocationItem.item_id == d.item_id)).with_lockmode("update").one()
                location_item.qty -= d.qty
                location_item.exp_qty -= d.qty
                location_item.area -= d.area
                location_item.exp_area -= d.area
                location_item.weight -= d.weight
                location_item.exp_weight -= d.weight

            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for(".view", action = "in_note"))


    @templated('inventory/out_note_index.html')
    def out_note(self):
        if _g('SEARCH_SUBMIT'):  # come from search
            values = {'page' : 1}
            for f in ['no', 'customer_id', 'create_time_from', 'create_time_to', 'location_id' ] :
                values[f] = _g(f)
        else: #come from paginate or return
            values = session.get('inventory_out_note_values', {})
            if _g('page') : values['page'] = int(_g('page'))
            elif 'page' not in values : values['page'] = 1
        if not values.get('create_time_from', None) and not values.get('create_time_to', None):
            values['create_time_to'] = dt.now().strftime("%Y-%m-%d")
            values['create_time_from'] = (dt.now() - timedelta(days = 30)).strftime("%Y-%m-%d")

        session['inventory_out_note_values'] = values
        conditions = [InventoryOutNote.active == 0]


        if values.get('create_time_from', None):       conditions.append(InventoryOutNote.create_time > values['create_time_from'])
        if values.get('create_time_to', None):         conditions.append(InventoryOutNote.create_time < '%s 23:59' % values['create_time_to'])
        if values.get('no', None):
            conditions.append(InventoryOutNote.no.op('ilike')('%%%s%%' % values['name']))
        if values.get('customer_id', None):
            conditions.append(InventoryOutNote.customer_id == values['customer_id'])
        if values.get('location_id', None):
            conditions.append(InventoryOutNote.customer_id == values['location_id'])
        result = DBSession.query(InventoryOutNote).filter(and_(*conditions)).order_by(desc(InventoryOutNote.create_time))

        def url_for_page(**params): return url_for('.view', action = "out_note", page = params['page'])
        records = paginate.Page(result, values['page'], show_if_single_page = True, items_per_page = PAGINATE_PER_PAGE, url = url_for_page)

        root_locations = DBSession.query(InventoryLocation).filter(and_(InventoryLocation.active == 0,
                                                       InventoryLocation.parent_id == None)).order_by(InventoryLocation.name)
        return {
                'values' : values ,
                'records' : records,
                'locations' : root_locations,
                }


    @templated('inventory/out_note_review.html')
    def out_note_review(self):
        id = _g('id')
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(self.default())
        obj = DBSession.query(InventoryOutNote).get(id)
        return {'obj' : obj}


    @templated('inventory/out_note_new.html')
    def out_note_new(self):
        ids = _gl('note_ids')
        records = DBSession.query(InventoryLocationItem).filter(and_(InventoryLocationItem.active == 0, InventoryLocationItem.id.in_(ids))).order_by(InventoryLocationItem.item_id)
        return {
                "records" : records,
                }


    def out_note_save_new(self):
        params = {}
        for f in ["customer_id", "so", "po", "dn", "ref", "remark", ]: params[f] = _g(f)
        try:
            header = InventoryOutNote(**params)
            DBSession.add(header)
            DBSession.flush()
            total_qty = total_area = total_weight = 0
            for k, id in _gp("item_"):
                tmp_qty = int(_g('qty_%s' % id) or 0)
                tmp_area = float(_g('area_%s' % id) or 0)
                tmp_weight = float(_g('weight_%s' % id) or 0)

                total_qty += tmp_qty
                total_area += tmp_area
                total_weight += tmp_weight

                tmp_location_item = DBSession.query(InventoryLocationItem).get(id)
                tmp_location_item.exp_qty -= tmp_qty
                tmp_location_item.exp_area -= tmp_area
                tmp_location_item.exp_weight -= tmp_weight

                DBSession.add(InventoryNoteDetail(
                                                  header_id = header.id,
                                                  type = 'OUT',
                                                  item_id = tmp_location_item.item_id,
                                                  desc = tmp_location_item.item.desc,
                                                  qty = tmp_qty,
                                                  weight = tmp_weight,
                                                  area = tmp_area,
                                                  remark = _g('remark_%s' % id),
                                                  location_id = tmp_location_item.location_id,
                                                  ))
            header.qty = total_qty
            header.weight = total_weight
            header.area = total_area
            header.no = getOutNo(header.id)

            DBSession.commit()
            flash(MSG_SAVE_SUCC, MESSAGE_INFO)
            return redirect(url_for('.view', action = "out_note_review", id = header.id))
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
            return redirect(url_for(".view", action = "index"))


    def out_note_approve(self):
        ids = _g('note_ids')
        if not ids :
            return {"code" : 1 , "msg" : MSG_NO_ID_SUPPLIED}
        flag = _g('flag')
        try:
            for r in DBSession.query(InventoryOutNote).filter(and_(InventoryOutNote.active == 0, InventoryOutNote.id.in_(ids.split("|")))):
                r.status = flag
                for d in r.details:

                    tmp_location_item = DBSession.query(InventoryLocationItem).filter(and_(InventoryLocationItem.item_id == d.item_id,
                                                                       InventoryLocationItem.location_id == d.location_id)).with_lockmode("update").one()

                    if flag == "1": # approve this out note
                        tmp_location_item.qty -= d.qty
                        tmp_location_item.area -= d.area
                        tmp_location_item.weight -= d.weight
                    elif flag == "2": #disapprove this out note
                        tmp_location_item.exp_qty += d.qty
                        tmp_location_item.exp_area += d.area
                        tmp_location_item.exp_weight += d.weight
            DBSession.commit()
            return jsonify({"code" : 0 , "msg" : MSG_SAVE_SUCC})
        except:
            DBSession.rollback()
            _error(traceback.print_exc())
            return jsonify({"code" : 1 , "msg" : MSG_SERVER_ERROR})


    def out_note_delete(self):
        id = _g(id)
        if not id :
            flash(MSG_NO_ID_SUPPLIED, MESSAGE_ERROR)
            return redirect(url_for(".view", action = "out_note"))
        try:
            note = DBSession.query(InventoryOutNote).get(id)
            note.active = 1
            for d in note.details:
                location_item = DBSession.query(InventoryLocationItem).filter(and_(InventoryLocationItem.active == 0,
                                                               InventoryLocationItem.location_id == d.location_id,
                                                               InventoryLocationItem.item_id == d.item_id)).with_lockmode("update").one()
                if note.status == 1 : # the record is not approved
                    location_item.qty += d.qty
                    location_item.area += d.area
                    location_item.weight += d.weight
                location_item.exp_qty += d.qty
                location_item.exp_area += d.area
                location_item.exp_weight += d.weight
            DBSession.commit()
            flash(MSG_DELETE_SUCC, MESSAGE_INFO)
        except:
            _error(traceback.print_exc())
            DBSession.rollback()
            flash(MSG_SERVER_ERROR, MESSAGE_ERROR)
        return redirect(url_for(".view", action = "out_note"))


bpInventory.add_url_rule('/', view_func = InventoryView.as_view('view'), defaults = {'action':'index'})
bpInventory.add_url_rule('/<action>', view_func = InventoryView.as_view('view'))
