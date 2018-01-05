# -*- coding: utf-8 -*-
from odoo import http

class AplicacionHa(http.Controller):
    @http.route('/aplicacion_ha/aplicacion_ha/', auth='public')
    def index(self, **kw):
        return "Hello, world"

    @http.route('/aplicacion_ha/print_ha/', auth='public')
    def view_report(self, **kw):
        #return "Hello, world"
        #html = "<html><head><title>Titulo tal</title></head><body><table><thead><tr><th>Encabe</th></tr></thead><tbody><tr><td>Body1</td></tr></tbody></table></body></html>"
        #return html
        #search_records = self.env['ha.model_ha'].search([])

        #sql = "SELECT * FROM table_name WHERE col = 'some_value'"

        '''
        html = "<html><head><title>Titulo tal</title></head><body><table><thead><tr><th>Encabe</th></tr></thead><tbody><tr><td>Body1</td></tr></tbody></table></body></html>"
        
        for item in search_records:
            html += "<tr><td>"+item+"</td></tr>"

        html += "</tbody></table></body></html>"
        return html
        '''

        '''
            self.env.cr.execute(sql)
            for record in self.env.cr.fetchall():
                # YOUR CODE HERE

                sql = "UPDATE table_name SET col = 'some_value' WHERE col = 'some_value'"
            self.env.cr.execute(sql)
            self.env.cr.commit()

            @api.multi
            def sql_example(self):
            sql = "SELECT * FROM table_name WHERE col = 'some_value'"

            self.env.invalidate_all()
        '''











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