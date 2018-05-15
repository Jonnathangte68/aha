# -*- coding: utf-8 -*-

from odoo import models, fields, api

import random
import string

class auxiliaractividadescambiantes(models.Model):
    _name = 'aha.auxiliaractividadescambiantes'

    name = fields.Char(
        string='Actividad',
        required=True,
    )

    actividadanterior = fields.Char(
        string='Actividad Anterior',
    )

    actividadnueva = fields.Char(
        string='Actividad Nueva',
    )

    semuestra = fields.Integer(
        string='Semuestra',
        default=0,
    )

    actividad_id = fields.Integer(
        string='Id de la actividad',
    )

    jefe_res_uid = fields.Integer(
        string='Jefe del usuario que cambio la actividad',
    )

    usuario_cambiante = fields.Char(
        string='Usuario que cambio la actividad',
    )

    @api.one
    def devolver(self):
        self.unlink()
        return True

    @api.one
    def autorizar(self):
        #activ = self.env['aha.activity'].search([('name','=',self.name)])
        #for ac in activ:
            #ac.write({'name':self.actividadnueva,'cambio':0,'aaa':None},1)
        #    print('ENTROOOOOOOOOOOOOOO A MODIFICARRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRRR')
        #    ac.write({'name':self.actividadnueva,'cambio':0,'aaa':None},123)
        #    print(ac)
        #print(activ)
        #print('Listtttttttttttttttttttttttttttttttttttttttttttttttt')
        #print(self.actividadnueva)
        #print(activ.name)
        #activ.write({'name':self.actividadnueva,'cambio':0,'aaa':None},1)
        #update con sql
        #result = self.env.cr.execute("SELECT resuser_id FROM aha_usuario WHERE login = 'maria.gamez'")
        #usuario_id = result.fetchone()
        #self.env.cr.execute("UPDATE aha_activity SET name = '"+self.actividadnueva+"' WHERE name = '"+self.actividadanterior+"'")
        #self.unlink()
        #raise Exception("El usuario indicado  "+str(self.usuario_cambiante))
        cursor_nuevo = self.env.cr
        cursor_nuevo.execute("SELECT rol_id FROM aha_usuario WHERE login = '"+self.usuario_cambiante+"' limit 1")
        uid = cursor_nuevo.fetchone()
        tiposhas = self.env['aha.tipoha'].search([('rol_id','=',uid)])
        for tha in tiposhas:
            for sec in tiposhas.section_ids:
                for acname in sec.activity_ids:
                    if acname.name == self.actividadanterior:
                        self.env.cr.execute("UPDATE aha_activity SET name = '"+self.actividadnueva+"' WHERE id = "+str(acname.id))
        #usuario_id = result.fetchone()
        # Con el rol recorrer el tipo de ha de ese rol y recorrer las secciones de esos tipos de HA y recorrer las actividades de esas secciones y si la actividad tiene el mismo nombre modificarla con sql
        #raise Exception("El usuario indicado  "+str(usuario_id))
        self.unlink()
        return True

    def get_id(self):
        cadenaaletoria = ""

        for n in range(32):
            aleatorio = random.choice(string.ascii_letters + string.digits)
            cadenaaletoria += aleatorio

        return cadenaaletoria
