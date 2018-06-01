# -*- coding: utf-8 -*-
from odoo import http
import xlsxwriter
import xlwt
from datetime import datetime
from io import BytesIO

class AplicacionHaEvaluateController(http.Controller):

    @http.route('/impresionexcel/evaluate/<condiciontiempo>/<rolee>', auth='public')
    def index(self,condiciontiempo,rolee, **kw):
        return '<html><head></head><body><p>Prueba</p></body><html>'