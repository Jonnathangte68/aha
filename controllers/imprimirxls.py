# -*- coding: utf-8 -*-
from odoo import http
from openerp.http import request
from openerp.addons.web.controllers.main import serialize_exception,content_disposition
import base64
import random
import string
import xlwt
from datetime import datetime
#from openpyxl import Workbook

class imprimirhojacontroller(http.Controller):
    @http.route('/aplicacion_ha/imprimirhojadeactividad/', auth='public')
    def index(self, **kw):

        style0 = xlwt.easyxf('font: name Times New Roman, color-index red, bold on',
            num_format_str='#,##0.00')
        style1 = xlwt.easyxf(num_format_str='D-MMM-YY')

        wb = xlwt.Workbook()
        ws = wb.add_sheet('A Test Sheet')

        ws.write(0, 0, 1234.56, style0)
        ws.write(1, 0, datetime.now(), style1)
        ws.write(2, 0, 1)
        ws.write(2, 1, 1)
        ws.write(2, 2, xlwt.Formula("A3+B3"))

        wb.save('example.xls')

        return 'Imprimio';