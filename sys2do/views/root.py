# -*- coding: utf-8 -*-
import traceback
import os
from datetime import datetime as dt
from flask import g, render_template, flash, session, redirect, url_for, request
from flaskext.babel import gettext as _
from sqlalchemy import and_

from sys2do import app
from sys2do.model import DBSession, User
from flask.helpers import jsonify
from sys2do.util.decorator import templated, login_required, has_all_permissions
from sys2do.util.common import _g, MESSAGE_ERROR, MESSAGE_INFO, upload
from sys2do.setting import UPLOAD_FOLDER, ALLOWED_EXTENSIONS, UPLOAD_FOLDER_URL





@templated("index.html")
def index():
#    flash('hello!', MESSAGE_INFO)
#    flash('SHIT!', MESSAGE_ERROR)
    app.logger.debug('A value for debugging')
    return {"content" : _("Hello,World!")}



