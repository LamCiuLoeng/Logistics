# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import datetime
import thread
from itertools import imap, ifilter
from jinja2.filters import do_default
from sys2do.constant import STATUS_LIST, SYSTEM_DATE_FORMAT, SYSTEM_DATETIME_FORMAT





__all__ = ['ft', 'fd', 'fn', 'ifFalse', 'f', 'showStatus', 'sum_with_none', 'map_city', 'map_province']


def ft(t, f = SYSTEM_DATETIME_FORMAT):
    try:
        return t.strftime(f)
    except:
        return '' if not t else str(t)


def fd(d, f = SYSTEM_DATE_FORMAT):
    try:
        return d.strftime(f)
    except:
        return '' if not d else str(d)


def fn(d, f = '%.2f'): return f % (d or 0)



def ifFalse(v, default = u""):
    return do_default(v, default) or default


f = ifFalse

def showStatus(s):
    for code, msg in STATUS_LIST:
        if s == code : return msg
    return ''


def sum_with_none(iterable, attribute = None):
    if attribute is not None:
        try:
            m = eval(attribute)
            iterable = imap(m, iterable)
        except:
            iterable = imap(lambda item : getattr(item, attribute), iterable)


    count = 0
    for k in iterable:
        try:
            count += k
        except:
            pass
    return count


_city_mapping = {}
_city_lock = thread.allocate_lock()
def map_city(city_id, default = ''):
    if not city_id : return default
    if not _city_mapping:
        with _city_lock:
            from sys2do.model import DBSession
            from sys2do.model.master import City
            for c in DBSession.query(City).filter(City.active == 0):
                _city_mapping[c.id] = unicode(c)
    return _city_mapping.get(city_id, default)



_province_mapping = {}
_province_lock = thread.allocate_lock()
def map_province(province_id, default = ''):
    if not province_id : return default
    if not _province_mapping:
        with _province_lock:
            from sys2do.model import DBSession
            from sys2do.model.master import Province
            for p in DBSession.query(Province).filter(Province.active == 0):
                _province_mapping[p.id] = unicode(p)
    return _province_mapping.get(province_id, default)

