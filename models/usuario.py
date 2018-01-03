# -*- coding: utf-8 -*-

from odoo import models, fields, api

class usuario(models.Model):
    _name = 'usuario'
    _inherit = 'res.users'

    name = fields.Char(
        string='Nombre',
        required=True,
    )

    apellido = fields.Char(
        string='Apellido',
        required=True,
    )

    fnacimiento = fields.Date(
        string='Fecha de Nacimiento',
    )

    email = fields.Char(
        string='Correo Electronico',
        required=False,
    )

    telefono = fields.Char(
        string='Telefono',
    )

    rol_id = fields.Many2one(
        string='Rol',
        comodel_name='rol',
    )

    @api.model
    def create(self, values):
        return super(usuario, self).create(values)