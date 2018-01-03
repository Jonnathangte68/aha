# -*- coding: utf-8 -*-

from odoo import models, fields, api

class evaljefe(models.Model):
    _name = 'evaljefe'

    fecha_revision = fields.Date(
        string='Fecha de Revision',
    )

    semana = fields.Integer(
        string='Semana',
    )

    criteriojefe_ids = fields.One2many(
        comodel_name='criteriojefe',
        inverse_name='evaljefe_id',
    )

    ha_id = fields.Many2one(
        comodel_name='ha',
    )