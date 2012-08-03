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
from datetime import date, datetime as dt
import urllib2
import json


from flask import g, render_template, flash, session, redirect, url_for, request
from werkzeug import secure_filename
from flask import current_app as app
from flaskext import babel

from sys2do.setting import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_URL, \
    SMS_KEY, SMS_FORMAT
from sys2do.model import DBSession, UploadFile
from sys2do.constant import MSG_RECORD_NOT_EXIST, MSG_NO_FILE_UPLOADED, \
    MSG_INVALID_FILE_TO_UPLOAD, SYSTEM_DATE_FORMAT, SYSTEM_DATETIME_FORMAT


__all__ = ['_g', '_gl', '_gp', '_debug', '_info', '_error', 'getOr404', 'upload', 'makeException', 'number2alphabet', 'date2text']




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



def check_mobile(no):
    if not no or not isinstance(no, basestring): return False
    if not no.isdigit() : return False
    if len(no) != 11 : return False #china mobile is 11 length
    if  no[:2] not in ['13', '15'] : return False
    return True


def send_sms(no, content):
    if not no or not content:
        return (2, "no NUMBER or no content is supplied!")

    try:
        if type(no) == str : no = [no, ]
        no = filter(lambda v : check_mobile(v) , no)
        if not no : return (2, "no NUMBER or no content is supplied!")

        sms_content = SMS_FORMAT % content
        url = "http://www.tui3.com/api/send/?k=%s&r=json&p=1&t=%s&c=%s" % (SMS_KEY, ",".join(no), sms_content)
        f = urllib2.urlopen(url)
        result = json.loads(f.read())
        print result

        if result['err_code'] == 0: return (0, 'success')
        else : return (1, result['err_msg'])

    except:
        _error(traceback.print_exc())
        return (1, 'error')



def date2text(value = None, dateTimeFormat = SYSTEM_DATETIME_FORMAT, defaultNow = False):
    if not value and defaultNow : value = dt.now()

    format = dateTimeFormat
    result = value

    if isinstance(value, date):
        try:
            result = value.strftime(format)
        except:
            traceback.print_exc()
    elif hasattr(value, "strftime"):
        try:
            result = value.strftime(format)
        except:
            traceback.print_exc()

    if not result:
        result = ""

    return result



if __name__ == "__main__":
    print send_sms(['13686488857', '15019200499'], '锐哥,我是阿良，下班了大家一齐去快乐的地方吧。')
