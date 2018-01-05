# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
#import wkhtmltopdf
#from wkhtmltopdf.main import WKhtmlToPdf

class ha(models.Model):
    _name = 'ha'

    name = fields.Char(
        string='Hoja de actividad',
    )

    # Tiene varias secciones 
    seccion_ids = fields.One2many(
        comodel_name='section',
        inverse_name='ha_id',
    )

    # Pertenece a un area
    area_id = fields.Many2one(
        comodel_name='area',
    )

    inicio_semana = fields.Integer(
        string='Del:',
        required=True,
    )

    fin_semana = fields.Integer(
        string='Al:',
        required=True
    )

    mes = fields.Selection(
        string='Mes',
        selection=[('enero', 'Enero'), ('febrero', 'Febrero'), ('marzo', 'Marzo'), ('abril', 'Abril'), ('mayo', 'Mayo'), ('junio', 'Junio'), ('julio', 'Julio'), ('agosto', 'Agosto'), ('septiembre', 'Septiembre'), ('octubre', 'Octubre'), ('noviembre', 'Noviembre'), ('diciembre', 'Diciembre')]
    )

    # Pertenece a un usuario el que esta logeado
    #usuario_id = fields.Many2one(
    #    comodel_name='model.name',
    #)

    evaljefe_id = fields.Many2one(
        comodel_name='evaljefe',
    )

    evalprocess_id = fields.Many2one(
        comodel_name='evalprocess',
    )

    @api.multi
    def print_ha(self):
        #payload = {'key1': 'value1', 'key2': ['value2', 'value3']}
        #r = requests.get(url='http://google.com')
        #r.url

        c = self.env.user
        #c.login login del usuario logeado

        sql = "SELECT ha.name, res_users.id, section.ha_id FROM ha, res_users, section, activity WHERE ha.id = section.ha_id AND activity.section_id = section.id AND login = "+c.login

        #print(sql)
        #result = ""
        self.env.cr.execute(sql)

        #wkhtmltopdf = WKhtmlToPdf(
        #    url='http://www.wikipedia.org',
        #    output_file='a.pdf',
        #)

        #c = self.env.user
        
        #for record in self.env.cr.fetchall():
        #  print(record)

        #raise Exception('Usuario actual: '+c.login)




