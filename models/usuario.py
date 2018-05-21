# -*- coding: utf-8 -*-

from odoo import models, fields, api
from openerp.exceptions import except_orm

class usuario(models.Model):
    _name = 'aha.usuario'
    #_inherit = 'res.users'

    name = fields.Char(
        string='Nombres',
        required=True
    )

    login = fields.Char(
        string='Apellidos',
        required=True
    )

    password = fields.Char(
        string='Cod. Empleado',
        required=True
    )

    rol_id = fields.Many2one(
        string='Rol',
        comodel_name='aha.rol',
    )

    calificacion_j = fields.Char(
        string='Calificacion asignada por el Jefe',
        readonly=True,
    )

    calificacion_p = fields.Char(
        string='Calificacion asignada por proceso',
        readonly=True,
    )

    area_id = fields.Many2one(
        string='Area',
        comodel_name='aha.area'
    )

    resuser_id = fields.Many2one(
        string='Id del usuario del Sistema',
        comodel_name='res.users',
    )

    jefe_id = fields.Many2one(
        string='A cargo de',
        comodel_name='aha.usuario',
        ondelete='cascade',
    )

    jefe_uid = fields.Integer(
        string='A cargo de',
        #default=lambda self: self.get_user_system_id()
    )

    def calcular_calificacion(self):

        print('SIIIIIIIIIIIIIIIIIIIIIIIIII ENTROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')

        l = self.env.context.get('u')

        print(l)

        calificacion_calculada2 = ""
        calificacion_calculada = "NO CALCULADA"






        rest_id = self.env['aha.usuario'].search([('login','=',l)]).resuser_id.id
        #has_list = self.env['aha.ha'].search([('usuario_id','=',rest_id)],order='create_date desc')
        print('Usuario del Login Listaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (usuario_id): ')
        print(rest_id)
        cf = ""
        counter = 0
        sql = "SELECT calificacion_general FROM AHA_EVALJEFE INNER JOIN AHA_HA ON AHA_HA.EVALJEFE_ID = AHA_EVALJEFE.ID WHERE AHA_HA.create_uid = "+str(rest_id)+" ORDER BY AHA_HA.create_date DESC"
        self.env.cr.execute(sql)
        for record in self.env.cr.fetchall():
            print('RECORDDDDDDDDDDDDDDDD ON 0')
            print(record[0])
            bandera = False
            if cf == "":
                cf = record[0]
            else:
                if record[0] == cf and bandera == False:
                    counter += 1
                else:
                    bandera = True
                
        print('ACAAAAAAAAAAAAAAAA RESULT       SFINALLLLLLLLLLLLLLLLLLL')
        print(cf+str(counter))
        calificacion_calculada2 = cf+str(counter)

        cf2 = ""
        counter2 = 0
        sql2 = "SELECT calificacion_general FROM AHA_EVALPROCESS INNER JOIN AHA_HA ON AHA_HA.EVALPROCESS_ID = AHA_EVALPROCESS.ID WHERE AHA_HA.create_uid = "+str(rest_id)+" ORDER BY AHA_HA.create_date DESC"
        self.env.cr.execute(sql2)
        for record2 in self.env.cr.fetchall():
            bandera2 = False
            if cf2 == "":
                cf2 = record2[0]
            else:
                if record2[0] == cf2 and bandera2 == False:
                    counter2 += 1
                else:
                    bandera2 = True
                
        calificacion_calculada = cf2+str(counter2)

        #Buscar al usuario, buscar el jefe del usuario y verificar si rest_id es igual al usuario logeado
        rest_jefe_id = self.env['aha.usuario'].search([('login','=',l)]).jefe_id.resuser_id.id
        print('Acaaaaaaaaaaaaaaaaaaaaaaaaaaa *----------------------* Prueba')
        print('Ha del usuario Jefeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee')
        print(rest_jefe_id)
        print('Ha del usuario en sistema -----------------------------------------------------------------')
        print(self.env.user.id)
        if rest_jefe_id == self.env.user.id:
            #951
            return {
                'name': 'Resultado de la Evaluacion de Hoja de Actividad',
                'view_mode': 'form',
                'view_id': self.env.ref('aha.formulario_detll_jefe').id,
                'view_type': 'form',
                'res_model': 'aha.usuario',
                'type': 'ir.actions.act_window',
                'target': 'self',
                'context': {
                    'default_name': l,
                    #'default_calificacion_j': data_ventana[1],
                    #'default_calificacion_p': data_ventana[2],
                    'default_calificacion_j': calificacion_calculada2,
                    'default_calificacion_p': calificacion_calculada,
                }
            }
        else:
            raise except_orm(('Notificacion!'),('No tiene permisos para ver la informacion de este usuario'))

    def calcular_calificacion_p(self):


        print('SIIIIIIIIIIIIIIIIIIIIIIIIII ENTROOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOOO')

        l = self.env.context.get('u')

        print(l)

        calificacion_calculada2 = ""
        calificacion_calculada = "NO CALCULADA"
        rest_id = self.env['aha.usuario'].search([('login','=',l)]).resuser_id.id
        print('Usuario del Login Listaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa (usuario_id): ')
        print(rest_id)
        cf2 = ""
        counter2 = 0
        sql2 = "SELECT calificacion_general FROM AHA_EVALPROCESS INNER JOIN AHA_HA ON AHA_HA.EVALPROCESS_ID = AHA_EVALPROCESS.ID WHERE AHA_HA.create_uid = "+str(rest_id)+" ORDER BY AHA_HA.create_date DESC"
        self.env.cr.execute(sql2)
        for record2 in self.env.cr.fetchall():
            bandera2 = False
            if cf2 == "":
                cf2 = record2[0]
            else:
                if record2[0] == cf2 and bandera2 == False:
                    counter2 += 1
                else:
                    bandera2 = True
                
        calificacion_calculada = cf2+str(counter2)

        return {
            'name': 'Resultado de la Evaluacion de Hoja de Actividad',
            'view_mode': 'form',
            'view_id': self.env.ref('aha.formulario_detll_proprocc').id,
            'view_type': 'form',
            'res_model': 'aha.usuario',
            'type': 'ir.actions.act_window',
            'target': 'self',
            'context': {
                'default_name': l,
                #'default_calificacion_p': data_ventana[1],
                'default_calificacion_p': calificacion_calculada,
            }
        }

    _sql_constraints = [
        ('uniq_name', 'unique(name)', "Ya existe un usuario registrado con el mismo nombre!"),
    ]

    @api.multi
    @api.onchange('jefe_id')
    def update_resjefe_uid(self):
        print('Entro al on change')
        print('EL idddddddddddddddddd que quierdddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddddd')
        print(self.jefe_id.resuser_id.id)
        self.jefe_uid = self.jefe_id.resuser_id.id
        print('El ultimo idddddddddddddddddddddddddddddddddddddddddddddddddddd')
        print(self.jefe_uid)

    @api.multi
    def calcular_calificacion_asignadas_x_jefes(self):
        users = self.env['aha.usuario'].search([])
        for u in users:

            # FORMA EL SQL


            #print(u.name)
            condicion_or = ""
            final_sql = " ORDER BY CREATE_DATE DESC"
            select_header = "SELECT calificacion_general FROM aha_evaljefe WHERE "
            has = self.env['aha.ha'].search([])
            i = 0
            sin_ha = False
            for ha in has:
                if ha.usuario_id.id == u.id:
                    if i == 0:
                        condicion_or += ("ha_id = "+str(ha.id))
                        i+=1
                        sin_ha = True
                    else:
                        condicion_or += (" or ha_id = "+str(ha.id))
                        i+=1
                        sin_ha = True
            #condition_or = condition_or + " ORDER BY CREATE_DATE DESC"
            string_condicion = str(condicion_or)
            #print(string_condicion)
            string_condicion += final_sql
            select_header += string_condicion
            #print(select_header)

            # EJECUTA EL SQL
            #letra = ""
            numero = 1
            acumulado = ""

            if sin_ha:
                cr = self.env.cr
                cr.execute(select_header)
                res = cr.fetchall()
                #print(res)
                for calf in res:
                    #print(calf[0])
                    if calf[0]:
                        if acumulado == "":
                            acumulado = calf[0]
                        else:
                            if acumulado == calf[0]:
                                numero += 1

            if acumulado:
                acumulado += str(numero)
                if acumulado != "":
                    u.write({'calificacion_j':acumulado})

    @api.multi
    def calcular_calificacion_asignadas_x_procesos(self):
        users = self.env['aha.usuario'].search([])
        for u in users:

            # FORMA EL SQL


            #print(u.name)
            condicion_or = ""
            final_sql = " ORDER BY CREATE_DATE DESC"
            select_header = "SELECT calificacion_general FROM aha_evalprocess WHERE "
            has = self.env['aha.ha'].search([])
            i = 0
            sin_ha = False
            for ha in has:
                if ha.usuario_id.id == u.id:
                    if i == 0:
                        condicion_or += ("ha_id = "+str(ha.id))
                        i+=1
                        sin_ha = True
                    else:
                        condicion_or += (" or ha_id = "+str(ha.id))
                        i+=1
                        sin_ha = True
            #condition_or = condition_or + " ORDER BY CREATE_DATE DESC"
            string_condicion = str(condicion_or)
            #print(string_condicion)
            string_condicion += final_sql
            select_header += string_condicion
            #print(select_header)

            # EJECUTA EL SQL
            #letra = ""
            numero = 1
            acumulado = ""

            if sin_ha:
                cr = self.env.cr
                cr.execute(select_header)
                res = cr.fetchall()
                #print(res)
                for calf in res:
                    #print(calf[0])
                    if calf[0]:
                        if acumulado == "":
                            acumulado = calf[0]
                        else:
                            if acumulado == calf[0]:
                                numero += 1

            if acumulado:
                acumulado += str(numero)
                if acumulado != "":
                    u.write({'calificacion_p':acumulado})
