# -*- coding: utf-8 -*-

from odoo import models, fields, api

class evalprocess(models.Model):
    _name = 'evalprocess'

    #autogenerar este con el nombredelusuario y la semana de la hoja de actividad
    name = fields.Char(
        string='Evaluacion',
    )

    #autocalculado en base a los criterios
    calificacion_general = fields.Char(
        string='Calificacion general',
    )

    criteriosprocess_ids = fields.One2many(
        string='Criterios',
        comodel_name='criterioprocess',
        inverse_name='evalprocess_id',
    )

    ha_id = fields.Many2one(
        comodel_name='ha',
    )