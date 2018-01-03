# -*- coding: utf-8 -*-

from odoo import models, fields, api

class criterioprocess(models.Model):
    _name = 'criterioprocess'

    name = fields.Char(
        string='Criterio de Evaluacion',
    )

    # 1 a muchos
    responsable = fields.Char(
        string='Responsable',
    )

    cumple = fields.Boolean(
        string='Cumple',
        required='False'
    )

    valor = fields.Integer(
        string='Valor',
        required=True,
    )

    comentario = fields.Char(
        string='Comentarios',
        required=False,
        
    )

    evalprocess_id = fields.Many2one(
        string='Evaluacion',
        comodel_name='evalprocess',
    )