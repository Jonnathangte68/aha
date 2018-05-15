# -*- coding: utf-8 -*-

from odoo import models, fields, api

class section(models.Model):
    _name = 'aha.section'

    name = fields.Char(
        string='Titulo de la Seccion',
        required=True
    )

    activity_ids = fields.One2many(
        string='Actividades',
        comodel_name='aha.activity',
        inverse_name='section_id',
    )

    ha_id = fields.Many2one(
        comodel_name='aha.ha',
    )

    usuario_id = fields.Many2one(
        string='Usuario',
        comodel_name='aha.usuario',
    )

    tipoha_id = fields.Many2one(
        string='Tipo de Ha x rol',
        comodel_name='aha.tipoha',
    )