# -*- coding: utf-8 -*-
from odoo import http
from openerp.http import request
#from . import models
import json
import xlsxwriter
import xlwt
from datetime import datetime
from io import BytesIO
from flask import Flask, send_file
try:
    from StringIO import StringIO
except ImportError:
    from io import StringIO

app = Flask(__name__)

class AplicacionHa(http.Controller):
    @http.route('/aplicacion_ha/probardesc', auth='public')
    def index(self, **kw):

        strIO = StringIO.StringIO()
        strIO.write('Hello from Dan Jacob and Stephane Wirtel !')
        strIO.seek(0)
        return send_file(strIO,
                         attachment_filename="testing.txt",
                         as_attachment=True)
        
app.run(debug=True)