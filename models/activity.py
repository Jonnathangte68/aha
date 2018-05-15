# -*- coding: utf-8 -*-

from odoo import models, fields, api

import random
import string

class activity(models.Model):
    _name = 'aha.activity'

    name = fields.Char(
        string='Actividad',
        #size=62,
        required=True,
    )
    um = fields.Selection(
        string='UM*',
        selection=[('Chk', 'Chk'), ('Ton', 'Ton - Total de toneladas'), ('#', '# Numero de Evento o unidades'), ('Per', 'Per - Personas'), ('Min', 'Min - Minutos'), ('Hrs', 'Hrs - Horas'), ('%', '% Porcentaje'), ('Firma', 'Firma'), ('% / Min', '% / Min'), ('# / Min', '# / Min'),('% / # / Min', '% / # / Min'),('% / %/ Min', '% / %/ Min'),('# / # / Min', '# / # / Min')],
    )
    frecuencia = fields.Selection(
        string='Frecuencia',
        selection=[('dia', 'Dia'), ('men', 'Men'), ('sem', 'Sem'), ('cat', 'Cat'), ('lun', 'Lun'), ('mar', 'Mar'), ('mie', 'Mie'), ('jue', 'Jue'), ('vie', 'Vie'), ('sab', 'Sab'), ('diario', 'Diario'),('evento', 'Por evento'), ('usm', '1er-Sem-Mes'), ('ssm', '2da-Sem-Mes'), ('tsm', '3er-Sem-Mes'), ('csm', '4ta-Sem-Mes')],
        #selection=[('dia', 'Diario'), ('evento', 'Por evento'), ('mensual', 'Mensual'), ('sabcustom', 'Sabado 08:00 a 13:00')]
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

    section_id = fields.Many2one(
        string='Seccion',
        comodel_name='aha.section',
    )

    typo = fields.Selection(
        string='Tipo de Actividad',
        default=0,
        selection=[(0, 'Actividad Regular'),(1, 'Actividad Base')]
    )

    cambio = fields.Integer(
        string='Si se modifico o no',
        default=0
    )

    aaa = fields.Char(
        string='Actividad Anterior',
    )

    auxfrecuencia = fields.Char(
        string='Hrs Programada:',
        required=False,
        readonly=False,
    )

    #on create
    @api.model
    def create(self, values):
        print('CREATE ACTIVITYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
        #print('Valores test my testttttttttttttttttttttttttttttttttttttttttttt mario fff')
        #print(values)
        creado = super(activity, self).create(values)
        return creado

    @api.model
    #on edit
    def write(self, values,cambio=None):


        miactivanteriornbr = self.name

        print('REEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEEE')


        res = super(activity, self).write(values)
        uid = self.env.user.id
        cr = self.env.cr
        crDos = self.env.cr
        name = values['name']
        um = values['um']
        frecuencia = values['frecuencia']
        lun = 't' if values['lun'] else 'f'
        mar = 't' if values['mar'] else 'f'
        miercol = 't' if values['miercol'] else 'f'
        juev = 't' if values['juev'] else 'f'
        viern = 't' if values['viern'] else 'f'
        sabad = 't' if values['sabad'] else 'f'
        #typo = values['typo']
        auxfrecuencia = '' if not values['auxfrecuencia'] else values['auxfrecuencia']
        secuencia = values['secuencia']

        # Traer rol y tipo de Ha
        roles = self.env['aha.usuario'].search([('resuser_id','=',self.env.user.id)]).rol_id
        usuario_mio = self.env['aha.usuario'].search([('resuser_id','=',self.env.user.id)])
        #modifica_nombre = False
        #actividad_normal = False
        ya_entro = False
        for rol in roles:
            for tipoHa in rol.tipoha_id:
                #print(tipoHa.section_ids)

                for secs in tipoHa.section_ids:
                    for activities in secs.activity_ids:
                        if activities.typo == 1 and values['name'] == activities.name:
                            print(self.name + "              VALUES                                       "+ str(values))
                            print("Entra 1 ___________________________________________________________________________________________________________")
                            cr.execute("UPDATE AHA_ACTIVITY SET um = '"+str(um)+"', frecuencia = '"+str(frecuencia)+"', lun = '"+lun+"', mar = '"+mar+"', miercol = '"+miercol+"', juev = '"+juev+"', viern = '"+viern+"', sabad = '"+sabad+"', secuencia = "+str(secuencia)+",auxfrecuencia = '"+auxfrecuencia+"' WHERE name like '%"+str(self.name)+"%' AND create_uid = '"+str(self.env.user.id)+"'")
                            cr.execute("UPDATE AHA_ACTIVITY SET um = '"+str(um)+"', frecuencia = '"+str(frecuencia)+"', lun = '"+lun+"', mar = '"+mar+"', miercol = '"+miercol+"', juev = '"+juev+"', viern = '"+viern+"', sabad = '"+sabad+"', secuencia = "+str(secuencia)+",auxfrecuencia = '"+auxfrecuencia+"' WHERE name like '%"+str(self.name)+"%' AND create_uid = '"+str(18)+"'")
                            print('Valor de ya entro ' + str(ya_entro))
                            if ya_entro == False:
                                self.env['aha.auxiliaractividadescambiantes'].create({'name':self.name, 'actividadanterior':miactivanteriornbr, 'actividadnueva':values['name'],'jefe_res_uid':usuario_mio.jefe_id.resuser_id.id,'usuario_cambiante':usuario_mio.name})
                                ya_entro = True
                        elif values['name'] == activities.name:
                            print(self.name + "              VALUES                                       "+ str(values))
                            print("Entra 2 ___________________________________________________________________________________________________________")
                            #cr.execute("UPDATE AHA_ACTIVITY SET um = '"+str(um)+"', frecuencia = '"+str(frecuencia)+"', name = '"+str(name)+"', lun = '"+lun+"', mar = '"+mar+"', miercol = '"+miercol+"', juev = '"+juev+"', viern = '"+viern+"', sabad = '"+sabad+"', secuencia = "+str(secuencia)+",auxfrecuencia = '"+auxfrecuencia+"' WHERE id = "+str(activities.id))
                            crDos.execute("UPDATE AHA_ACTIVIDADESAGREGADASPORELUSUARIO SET um = '"+str(um)+"', name = '"+str(name)+"', frecuencia = '"+str(frecuencia)+"', secuencia = "+str(secuencia)+", lun = '"+lun+"', mar = '"+mar+"', miercol = '"+miercol+"', juev = '"+juev+"', viern = '"+viern+"', sabad = '"+sabad+"', auxfrecuencia = '"+auxfrecuencia+"' WHERE name like '%"+str(self.name)+"%' and create_uid = "+str(self.env.user.id))
                            
        return res

    def get_id(self):
        cadenaaletoria = ""

        for n in range(32):
            aleatorio = random.choice(string.ascii_letters + string.digits)
            cadenaaletoria += aleatorio

        return cadenaaletoria