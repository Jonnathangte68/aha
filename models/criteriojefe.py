# -*- coding: utf-8 -*-

from odoo import models, fields, api

class criteriojefe(models.Model):
    _name = 'criteriojefe'

    name = fields.Char(
    	string='Utilizacion de la hoja de actividad'
    )

    cumple = fields.Boolean(
        string='Cumple',
    )

    comentarios = fields.Text(
        string='Comentarios',
    )

    evaljefe_id = fields.Many2one(
        comodel_name='evaljefe',
    )
