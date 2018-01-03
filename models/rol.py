# -*- coding: utf-8 -*-

from odoo import models, fields, api

#Rol o Grupo Ver como enlazar con odoo groups
class rol(models.Model):
	_name = 'rol'

	name = fields.Char(
	    string='Nombre del Rol',
	    required=True,
	)

	#usuario_ids = fields.One2many(
	#    string='Usuario',
	#    comodel_name='usuario',
	#    inverse_name='rol_id',
	#)