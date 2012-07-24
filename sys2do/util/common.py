# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import os
import traceback
from datetime import datetime as dt
from flask import g, render_template, flash, session, redirect, url_for, request
from werkzeug import secure_filename
from flask import current_app as app
from flaskext import babel

from sys2do.setting import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_URL
from sys2do.model import DBSession, UploadFile
from sys2do.constant import MSG_RECORD_NOT_EXIST, MSG_NO_FILE_UPLOADED, \
    MSG_INVALID_FILE_TO_UPLOAD


__all__ = ['_g', '_gl', '_gp', '_debug', '_info', '_error', 'getOr404', 'upload', 'makeException', 'number2alphabet']




def _g(name, default = None):
    return request.values.get(name, default) or None

def _gl(name):
    return request.form.getlist(name)

def _gp(prefix):
    return sorted([(k, v or None) for k, v in request.values.items() if k.startswith(prefix)], cmp = lambda x, y: cmp(x[0], y[0]))

def _allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


_debug = lambda msg : app.logger.debug(msg)

_info = lambda msg : app.logger.debug(msg)

_error = lambda msg : app.logger.debug(msg)


def getMasterAll(obj, order_by = 'name'):
    if isinstance(obj, basestring) :
        import sys2do.model as mymodel
        obj = getattr(mymodel, obj)
    return DBSession.query(obj).filter(obj.active == 0).order_by(getattr(obj, order_by)).all()


def getOr404(obj, id, redirect_url = "/index", message = MSG_RECORD_NOT_EXIST):
    try:
        v = DBSession.query(obj).get(id)
        if v : return v
        else : raise makeException(message)
    except:
        traceback.print_exc()
        flash(message)
        return redirect(redirect_url)


def upload(name):
    f = request.files.get(name, None)
    if not f : raise makeException(MSG_NO_FILE_UPLOADED)
    if _allowedFile(f.filename):
        if not os.path.exists(UPLOAD_FOLDER) : os.makedirs(UPLOAD_FOLDER)
        converted_name = "%s.%s" % (dt.now().strftime("%Y%m%d%H%M%S"), f.filename.rsplit('.', 1)[1].lower())
        path = os.path.join(UPLOAD_FOLDER, converted_name)
        f.save(path)

        u = UploadFile(create_by_id = session['user_profile']['id'], name = secure_filename(f.filename), path = path, url = "/".join([UPLOAD_FOLDER_URL, converted_name]))
        DBSession.add(u)
        DBSession.flush()
        return u
    else:
        raise makeException(MSG_INVALID_FILE_TO_UPLOAD)


def makeException(msg):
    class _ExceptionClz(Exception):
        def __init__(self, msg = msg):
            self.msg = msg
            self.is_customize = True

        def __str__(self): return self.msg
        def __unicode__(self): return self.msg
        def __repr__(self): return self.msg

    return _ExceptionClz



def number2alphabet(n):
    result = []
    while n > 0 :
        x , y = n / 26, n % 26
        result.append(y)
        if x > 0 :
            n = x
        else:
            break

    p = 0
    for i in range(len(result)):
        result[i] += p
        if result[i] <= 0 and i + 1 < len(result):
            result[i] += 26
            p = -1
        else:
            p = 0

    if result[-1] <= 0 : result = result[:-1]
    result.reverse()
    return "".join(map(lambda v:chr(v + 64), result))

