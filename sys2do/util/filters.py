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
#from flask import current_app as app
#from sys2do import app

__all__ = ['ft', 'fd', 'ifFalse']


def ft(t, f = "%Y-%m-%d %H:%M:%S"):
    try:
        return t.strftime(f)
    except:
        return str(t)


def fd(d, f = "%Y-%m-%d"):
    try:
        return d.strftime(f)
    except:
        return str(d)


def ifFalse(v, default = u""):
    return do_default(v, default) or default
