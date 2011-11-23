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

__all__ = ['todayBefore', 'formatTime', 'formatDate', 'string2Date', 'ifFalse', 'getByID']


def todayBefore(d):
    if type(d) == datetime.datetime : return d < datetime.datetime.today()
    if type(d) == datetime.date : return d <= datetime.datetime.today().date()
    return False



def formatTime(t, f = "%Y-%m-%d %H:%M%S"):
    try:
        return t.strftime(f)
    except:
        return str(t)


def formatDate(d, f = "%Y-%m-%d"):
    try:
        return d.strftime(f)
    except:
        return str(d)


def string2Date(v):
    return "%s-%s-%s" % (v[:4], v[4:6], v[-2:])

def ifFalse(v, default = u""):
    return do_default(v, default) or default


def getByID(id, obj, attr):
    from sys2do.model import DBSession
    from sys2do import model as dbModel
    v = getattr(DBSession.query(getattr(dbModel, obj)).get(id), attr)
    return v() if callable(v) else v
