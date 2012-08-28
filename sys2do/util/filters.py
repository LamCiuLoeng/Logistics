# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import datetime
from itertools import imap, ifilter
from jinja2.filters import do_default
from sys2do.constant import STATUS_LIST, SYSTEM_DATE_FORMAT, SYSTEM_DATETIME_FORMAT



__all__ = ['ft', 'fd', 'fn', 'ifFalse', 'f', 'showStatus', 'sum_with_none']


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

