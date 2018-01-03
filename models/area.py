# -*- coding: utf-8 -*-

from odoo import models, fields, api

class area(models.Model):
    _name = 'area'

    name = fields.Char(
        string='Nombre',
        required=True,
        readonly=True
    )

    fecha_corte = fields.Datetime(
        string='Fecha corte',
    )