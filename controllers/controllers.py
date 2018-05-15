# -*- coding: utf-8 -*-
from odoo import http
import xlsxwriter
import xlwt
from datetime import datetime
from io import BytesIO

class AplicacionHa(http.Controller):
    @http.route('/aplicacion_ha/aplicacion_ha/', auth='public')
    def index(self, **kw):
        return "Hello, world"
        

    @http.route('/aplicacion_ha/print_ha/', auth='public')
    def view_report(self, **kw):
        return 'nada aun'

    @http.route('/evaluacion-ha/<cuno>/<cdos>', auth='public')
    def evaluacion_ha(self, cuno, cdos, **kw):
        return '<html><body><h1>'+cuno+'</h1></body></html>'