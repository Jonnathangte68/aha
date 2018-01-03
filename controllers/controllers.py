# -*- coding: utf-8 -*-
from odoo import http

# class AplicacionHa(http.Controller):
#     @http.route('/aplicacion_ha/aplicacion_ha/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/aplicacion_ha/aplicacion_ha/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('aplicacion_ha.listing', {
#             'root': '/aplicacion_ha/aplicacion_ha',
#             'objects': http.request.env['aplicacion_ha.aplicacion_ha'].search([]),
#         })

#     @http.route('/aplicacion_ha/aplicacion_ha/objects/<model("aplicacion_ha.aplicacion_ha"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('aplicacion_ha.object', {
#             'object': obj
#         })