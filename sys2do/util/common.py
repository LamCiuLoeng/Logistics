# -*- coding: utf-8 -*-
'''
###########################################
#  Created on 2011-10-25
#  @author: cl.lam
#  Description:
###########################################
'''
import os
from datetime import datetime as dt
from flask import g, render_template, flash, session, redirect, url_for, request
from werkzeug import secure_filename
from flask import current_app as app
from flaskext import babel

from sys2do.setting import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_URL
from sys2do.model import DBSession, UploadFile
import traceback
from sys2do.constant import MSG_RECORD_NOT_EXIST, MSG_NO_FILE_UPLOADED, \
    MSG_INVALID_FILE_TO_UPLOAD

__all__ = ['_g', '_gl', '_gp', '_debug', '_info', 'getOr404', 'upload', 'makeException']




def _g(name, default = None):
    return request.values.get(name, default) or None

def _gl(name):
    return request.form.getlist(name)

def _gp(prefix):
    return sorted([(k, v or None) for k, v in request.values.items() if k.startswith(prefix)], cmp = lambda x, y: cmp(x[0], y[0]))

def _allowedFile(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def _debug(msg):
    app.logger.debug(msg)

def _info(msg):
    app.logger.debug(msg)




def getMasterAll(obj, order_by = 'name'):
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



