# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-11-23
#  @author: cl.lam
#  Description:
###########################################
'''
import traceback
from flaskext.babel import gettext as _
from flask import flash, redirect, render_template
from sys2do import app
from sys2do.util.common import _g, _gl, MESSAGE_ERROR, MESSAGE_INFO, makeException
from sys2do.model import DBSession
from sys2do.model.auth import CRUDMixin



__all__ = ['Handler', 'createHandler']


class Handler(object):

    def __init__(self,
                 dbClz,
                 name_for_url,
                 default_action = 'SEARCH',
                 action_name = 'action',
                 save_type_name = 'save_type',
                 redirect_url = "/index",
                 action_mapping = {}):

        self.dbClz = dbClz
        self.__name__ = name_for_url
        self.default_action = default_action
        self.action_name = action_name
        self.save_type_name = save_type_name
        self.redirect_url = redirect_url
        self.action_mapping = {
                              'SEARCH' : self.search,
                              'ADD' :    self.add,
                              'UPDATE' : self.update ,
                              'SAVE' :   self.save,
                              'DELETE' : self.delete,
                              }

        if action_mapping : self.action_mapping.update(action_mapping)


    def search(self):
        result = DBSession.query(self.dbClz).filter(self.dbClz.active == 0).all()
        return self._render_template('common/search.html', result = result)


    def add(self):
        return self._render_template('common/add.html')

    def update(self):
        id = _g('id')
        if not id :
            flash(_('No enough parameter(s) to make the operation!'))
            return redirect(self.redirect_url)
        obj = self.dbClz.get(id)
        values = obj.populate()
        return self._render_template('common/update.html', values = values)

    def save(self) :
        if isinstance(self.dbClz, CRUDMixin):
            save_type = _g(self.save_type_name)
            if save_type not in ['NEW', 'UPDATE']:
                flash(_('No such operation!'), MESSAGE_ERROR)
                return redirect(self.redirect_url)
            try:
                if save_type == 'NEW':
                    DBSession.add(self.dbClz.saveAsNew())
                    msg = _('Save the new record successfully!')
                elif save_type == 'UPDATE':
                    obj = DBSession.query(self.dbClz).get(_g('id'))
                    obj.saveAsUpdate()
                    msg = _('Update the record successfully!')
                DBSession.commit()
                flash(_(msg))
            except:
                app.logger.error(traceback.print_exc())
                DBSession.rollback()
                flash(_('The service is not available!'), MESSAGE_ERROR)
            else:
                return redirect(self.redirect_url)
        else:
            makeException('No save function for this object!')


    def delete(self) :
        try:
            DBSession.query(self.dbClz).get(_g('id')).active = 1
            DBSession.commit()
        except:
            app.logger.error(traceback.print_exc())
            DBSession.rollback()
            flash(_('The service is not available!'), MESSAGE_ERROR)
        else:
            flash(_('Delete the record successfully!'), MESSAGE_INFO)
        return redirect(self.redirect_url)


    def _render_template(self, template_name, **context):
        context['handler'] = self
        return render_template(template_name, **context)



    def __call__(self):
        app.logger.info(id(self))
        action = _g(self.action_name) or self.default_action
        if action not in self.action_mapping:
            flash(_('No such operation!'), MESSAGE_ERROR)
            return redirect(self.redirect_url)
        return self.action_mapping[action]()




def createHandler(dbClz, name_for_url, *args, **kw):
    _rf = lambda : Handler(dbClz, name_for_url, *args, **kw)()
    _rf.__name__ = name_for_url
    return _rf
