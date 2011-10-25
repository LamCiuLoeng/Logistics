# -*- coding: utf-8 -*-
from flask import render_template
from flask import current_app as app



error_page = lambda code : lambda error : render_template("%d.html" % code)
