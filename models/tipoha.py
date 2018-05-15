# -*- coding: utf-8 -*-

from odoo import models, fields, api

class tipoha(models.Model):
    _name = 'aha.tipoha'

    name = fields.Char(
        string='Tipo de HA',
    )

    section_ids = fields.One2many(
        string='Secciones',
        comodel_name='aha.section',
        inverse_name='tipoha_id',
    )

    rol_id = fields.Many2one(
        string='Rol Id',
        comodel_name='aha.rol',
        ondelete='cascade',
    )
