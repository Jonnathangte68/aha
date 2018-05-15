# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Rol o Grupo Ver como enlazar con odoo groups
class rol(models.Model):
    _name = 'aha.rol'

    name = fields.Char(
        string='Nombre del Rol',
        required=True,
    )

    tipoha_id = fields.One2many(
        comodel_name='aha.tipoha',
        inverse_name='rol_id'
    )

    usuario_ids = fields.One2many(
        string='Usuario Ids',
        comodel_name='aha.usuario',
        inverse_name='rol_id',
    )