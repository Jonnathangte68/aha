# -*- coding: utf-8 -*-

from odoo import models, fields, api

class section(models.Model):
    _name = 'section'

    name = fields.Char(
        string='Titulo de la Seccion',
    )

    activity_ids = fields.One2many(
        string='Actividades',
        comodel_name='activity',
        inverse_name='section_id',
    )

    ha_id = fields.Many2one(
        comodel_name='ha',
    )