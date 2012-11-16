# -*- coding: utf-8 -*-
from flask import render_template
from sys2do import app




error_page = lambda code : lambda error : render_template("%d.html" % code)


@app.errorhandler(500)
def server_error(error):
    from sys2do.util.common import _error
    _error(error)
    return render_template("%d.html" % 500)
