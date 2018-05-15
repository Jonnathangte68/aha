# -*- coding: utf-8 -*-
from odoo import http
from openerp.http import request
#from . import models
import json
import xlsxwriter
import xlwt
from datetime import datetime
from io import BytesIO

class AplicacionHa(http.Controller):
    @http.route('/aplicacion_ha/iniciar_sesion', auth='public')
    def index(self, **kw):

        #Get the cursor object
        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry
        #svalues = super(AplicacionHa, self).checkout_values()

        #print(request.params)
        usuario = request.params['usuario']
        contrasenia = request.params['contrasenia']
        #print(usuario)
        #print(contrasenia)
        #La consulta real se ejecuta asi
        #cr.execute('select * from res_partner where name = %s', (partner_name,))
        #sql = "select * from res_partner"
        #cursor = cr.execute(sql)
        #if cursor:
            #res = cursor.fetchall()
            #print('Resultado de la Consulta SQL: --*--')
            #print(res)
        #tmp_obj = request.registry('usuario');
        #request.env['usuario'].search(['', '=', ''])
        #fleet_vehicle_log_fuel_obj = pool.get('fleet_vehicle_log_fuel')
        #ids = tmp_obj.search(cr, uid, [])
        #tmp_obj = request.env['usuario'].search([])
        #for tmp in tmp_obj:
        #    print(tmp.login)
        #tmp_obj = request.env['usuario']
        #print(tmp_obj.get_all())
        #print(tmp_obj)
        if usuario == 'jonnathan' and contrasenia == '123':
            return json.dumps('1')
        else:
            return json.dumps('0')

    @http.route('/aplicacion_ha/get_users', auth='public')
    def listausuarios(self, **kw):

        cr, uid, context, registry = request.cr, request.uid, request.context, request.registry

        area_id = request.params['area']

        lista = ['nombre', 'codigo']

        return lista
      