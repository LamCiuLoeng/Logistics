# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import datetime
from jinja2.filters import do_default
from sys2do.constant import STATUS_LIST
#from flask import current_app as app
#from sys2do import app

__all__ = ['ft', 'fd', 'ifFalse', 'f', 'showStatus']


def ft(t, f = "%Y-%m-%d %H:%M"):
    try:
        return t.strftime(f)
    except:
        return '' if not t else str(t)


def fd(d, f = "%Y-%m-%d"):
    try:
        return d.strftime(f)
    except:
        return '' if not d else str(d)


def ifFalse(v, default = u""):
    return do_default(v, default) or default


f = ifFalse

def showStatus(s):
    for code, msg in STATUS_LIST:
        if s == code : return msg
    return ''
