# -*- coding: utf-8 -*-

from odoo import models, fields, api

class comment(models.Model):
    _name = 'comment'

    name = fields.Char()
    dia = fields.Selection(
        string='Dia',
        selection=[('l', 'Lunes'), ('m', 'Martes'), ('mi', 'Miercoles'), ('j', 'Jueves'), ('v', 'Viernes'), ('s', 'Sabado')]
    )
    comment_text = fields.Text(
        string='Comentario',
    )
    meta_text = fields.Text(
        string='Metas o Acciones',
    )