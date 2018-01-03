# -*- coding: utf-8 -*-

from odoo import models, fields, api

class activity(models.Model):
    _name = 'activity'

    name = fields.Char(
        string='Actividad',
        required=True,
    )
    um = fields.Selection(
        string='UM*',
        selection=[('min', 'Min'), ('num_min', '# / Min'), ('num', '#'), ('por_min', '% / Min'), ('por', '%'), ('hrs', 'Hrs')]
    )
    frecuencia = fields.Selection(
        string='Frecuencia',
        selection=[('dia', 'Diario'), ('evento', 'Por evento'), ('mensual', 'Mensual'), ('sabcustom', 'Sabado 08:00 a 13:00')]
    )
    lun = fields.Boolean(
        string='Lunes',
    )
    mar = fields.Boolean(
        string='Martes',
    )
    miercol = fields.Boolean(
        string='Miercoles',
    )
    juev = fields.Boolean(
        string='Jueves',
    )
    viern = fields.Boolean(
        string='Viernes',
    )
    sabad = fields.Boolean(
        string='Sabado',
    )

    section_id = fields.Many2one(
        string='Seccion',
        comodel_name='section',
    )