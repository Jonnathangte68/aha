# -*- coding: utf-8 -*-

from odoo import models, fields, api

import random
import string

class actividadesagregadasporelusuario(models.Model):
    _name = 'aha.actividadesagregadasporelusuario'

    name = fields.Char(
        string='Actividad',
        required=True,
    )
    um = fields.Char(
        string='UM*',
    )
    frecuencia = fields.Char(
        string='Frecuencia',
    )
    secuencia = fields.Float(
        string='Secuencia',
        default=-1,
        digits=(16, 2),
        help='Posicion de la Actividad en la Hoja de Actividad'
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

    section_id = fields.Integer(
        string='Seccion',
    )

    typo = fields.Integer(
        string='Tipo de Actividad',
    )

    cambio = fields.Integer(
        string='Si se modifico o no',
        default=0
    )

    aaa = fields.Char(
        string='Actividad Anterior',
    )

    auxfrecuencia = fields.Char(
        string='Frecuencia unica:',
        required=False,
        readonly=False,
    )
    # Para lo que se necesita
    actividad_id = fields.Char(
        string='actividad id',
    )

    usuario_id = fields.Integer(
        string='usuario id',
    )

    section_name = fields.Char(
        string='Nombre de la Seccion',
    )

    ha_id = fields.Char(
        string='ha id',
    )

    resuser_id = fields.Integer(
        string='Usuario del Id en el ERP',
    )

    status = fields.Integer(
        string='Estado',
    )

    @api.model
    def create(self, values):

        creado = super(actividadesagregadasporelusuario, self).create(values)
        #print('Create de actividades propias')
        #self.env['aha.activity'].search([('name','=',self.name),('um','=',self.um),('usuario_id','=',self.usuario_id)]).sudo().unlink()
        #print('Acaaaaaaaaaaaaaaaaaaaaaaaaa test')
        #print(self.name)
        #print(values)
        self.env['aha.actividadesagregadasporelusuario'].search([('name','=',self.name),('resuser_id','=',self.env.user.id)]).sudo().unlink()
        self.env['aha.activity'].search([('name','=',self.name),('um','=',self.um)]).sudo().unlink()
        return creado

    @api.model
    def write(self, values):
        print(values)
        res = super(actividadesagregadasporelusuario, self).write(values) #res stores the result of the write function
        #self.env['aha.activity'].search([('name','=',self.name),('create_uid','=',self.env.user.id)]).sudo().unlink()
        #self.env['aha.actividadesagregadasporelusuario'].search([('name','=',self.name),('create_uid','=',self.env.user.id)]).sudo().unlink()
        return res

    @api.one
    def eliminar_actividad(self):
        print('Eliminar Actividad')
        #env['res.partner'].sudo(public).search([])
        #admin = env.ref('base.public_user')
        #actividadeliminar = self.env['aha.activity'].search([('name','=',self.name)])
        self.env.cr.execute("DELETE FROM aha_activity WHERE id IN (select aha_activity.id from aha_activity inner join aha_section on aha_activity.section_id = aha_section.id inner join aha_ha on aha_section.ha_id = aha_ha.id inner join aha_usuario on aha_ha.usuario_id = aha_usuario.id where aha_usuario.resuser_id = "+str(self.env.user.id)+" and aha_activity.name = '"+str(self.name)+"')")
        self.env.cr.commit()
        self.env.cr.execute("DELETE FROM aha_actividadesagregadasporelusuario where name = '"+str(self.name)+"' and create_uid = '"+str(self.env.user.id)+"'")
        self.env.cr.commit()
        #self.env.cr.execute("delete from aha_activity inner join aha_section on aha_activity.section_id = aha_section.id inner join aha_ha on aha_section.ha_id = aha_ha.id inner join aha_usuario on aha_ha.usuario_id = aha_usuario.id where aha_usuario.resuser_id = "+str(self.env.user.id)+" and aha_ha.name = '"+str(self.name)+"'")
        #self.env.cr.commit()
        #print('List actividad eliminar')
        #print(actividadeliminar)
        #for a in actividadeliminar:
        #    if a.section_id.ha_id.usuario_id.resuser_id.id == self.env.user.id:
        #        # No funciona meter cursor
        #        #self.env.cr.execute("DELETE FROM aha_activity WHERE id = "+str(a.id)+";ALTER TABLE  DROP COLUMN ;")
        #        print('Borrado Query')
        #        print("DELETE FROM aha_activity WHERE id = "+str(a.id)+";")
        #        self.env.cr.execute("DELETE FROM aha_activity WHERE id = "+str(a.id)+";")
        #        self.env.cr.commit()
        #        print(' *-*-*-**-*-**-*-*-*-- Toda LA INFOOOOOOOOOOOOO aquiiiiiiiiiiiiiiiiiii *-*-*-*-*-*-*-*-*-*-***** ')
        #        print('Nombre de la actividad --------------------> Id de la actividad: '+str(a.id))
        #        print(a.name)
        #        print(a.section_id.ha_id.usuario_id.resuser_id)
        #        print(self.env.user.id)
        #a.sudo().unlink()
        #print('La actividad')
        #print(actividadeliminar)
        #actividadeliminar.sudo().unlink()
        #self.unlink()
        #actividadeliminar.unlink()