# -*- coding: utf-8 -*-
from flask import render_template
from sys2do import app



error_page = lambda code : lambda error : render_template("%d.html" % code)

#@app.before_request
#def checkLogin():
#    app.logger.debug('check logiin')
