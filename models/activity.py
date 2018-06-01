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
        #print('CREATE ACTIVITYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYYY')
        #print('Valores test my testttttttttttttttttttttttttttttttttttttttttttt mario fff')
        #print(values)

        creado = super(activity, self).create(values)
        #print("Actividad creadaaaa nueva")
        #print(creado)
        return creado

    @api.model
    #on edit
    def write(self, values,cambio=None):

        
        miactivanteriornbr = self.name

        if not self.typo or self.typo == 0:
            #La actividad no se agrega a la seccion -1
            #Es una actividad propia, sin tanto protocolo. No interesa cambio y no interesa nada mas, modificar SQL.
            crs_actividadespropias = self.env.cr
            #print("Consulta sql")
            #print("SELECT * FROM aha_actividadesagregadasporelusuario WHERE name = '"+str(self.name)+"' AND um = '"+str(self.um)+"' AND frecuencia = '"+str(self.frecuencia)+"'")
            crs_actividadespropias.execute("SELECT * FROM aha_actividadesagregadasporelusuario WHERE name = '"+str(self.name)+"' AND um = '"+str(self.um)+"' AND frecuencia = '"+str(self.frecuencia)+"'")
            r = crs_actividadespropias.fetchall()
            for item in r:
                #print("Entra tiene valores")
                bandera = 0
                cursor_internooo = self.env.cr
                #Formar SQL
                sql_yy = "UPDATE aha_actividadesagregadasporelusuario "
                if values['name']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET name = '"+str(values['name'])+"' "
                    else:
                        sql_yy += ", name = '"+str(values['name'])+"' "
                if values['secuencia']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET secuencia = "+str(values['secuencia'])+" "
                    else:
                        sql_yy += ", secuencia = "+str(values['secuencia'])+" "
                if values['um']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET um = '"+str(values['um'])+"' "
                    else:
                        sql_yy += ", um = '"+str(values['um'])+"' "
                if values['auxfrecuencia']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET auxfrecuencia = '"+str(values['auxfrecuencia'])+"' "
                    else:
                        sql_yy += ", auxfrecuencia = '"+str(values['auxfrecuencia'])+"' "
                if values['lun']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET lun = 't' "
                    else:
                        sql_yy += ", lun = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET lun = 'f' "
                    else:
                        sql_yy += ", lun = 'f' "                
                if values['mar']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET mar = 't' "
                    else:
                        sql_yy += ", mar = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET mar = 'f' "
                    else:
                        sql_yy += ", mar = 'f' "  
                if values['miercol']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET miercol = 't' "
                    else:
                        sql_yy += ", miercol = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET miercol = 'f' "
                    else:
                        sql_yy += ", miercol = 'f' "  
                if values['juev']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET juev = 't' "
                    else:
                        sql_yy += ", juev = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET juev = 'f' "
                    else:
                        sql_yy += ", juev = 'f' "  
                if values['viern']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET viern = 't' "
                    else:
                        sql_yy += ", viern = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET viern = 'f' "
                    else:
                        sql_yy += ", viern = 'f' "  
                if values['sabad']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET sabad = 't' "
                    else:
                        sql_yy += ", sabad = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy += "SET sabad = 'f' "
                    else:
                        sql_yy += ", sabad = 'f' "  
                sql_yy += "WHERE id = "+str(item[0])
                #Solo prueba 
                #print("Resultado de la consulta SQL")
                #print(sql_yy)
                cursor_internooo.execute(sql_yy)

        #print("Id actividad creada")
        #print(self.id)

        if self.typo == 1:
            crs_selusuarioproceso = self.env.cr
            crs_selusuarioproceso.execute("SELECT id FROM res_users WHERE login = 'proceso'")
            tmpselusuproceso = crs_selusuarioproceso.fetchone()
            id_usuario_procesos = tmpselusuproceso[0]
            crs_actividadespropias = self.env.cr
            crs_actividadespropias.execute("SELECT * FROM aha_activity WHERE name = '"+self.name+"' AND um = '"+self.um+"' AND frecuencia = '"+self.frecuencia+"' AND create_uid = "+str(id_usuario_procesos))
            rsp = crs_actividadespropias.fetchall()
            #print("La actividad de la seccion BASEEEEEEEEEEEEEEEE que se quiere cambiar")
            #print("SELECT * FROM aha_actividadesagregadasporelusuario WHERE name = '"+self.name+"' AND um = '"+self.um+"' AND frecuencia = '"+self.frecuencia+"' AND create_uid = "+str(id_usuario_procesos))
            #print(rsp)
            for actchanged in rsp:
                bandera = 0
                id_actividadacambiar = actchanged[0]
                crs_actividadespropias2 = self.env.cr
                sql_yy2 = "UPDATE aha_activity "
                if values['name']:
                    #Abrir consulta para crear traer el id de mi usuario y el res id del jefe
                    if self.name!=values['name']:
                        cursor_de_usuario = self.env.cr
                        cursor_de_usuario.execute("SELECT name, jefe_uid FROM AHA_USUARIO WHERE resuser_id = " + str(self.env.user.id))
                        valores_de_usuario = cursor_de_usuario.fetchone()
                        self.env['aha.auxiliaractividadescambiantes'].create({'name':self.name, 'actividadanterior':self.name, 'actividadnueva':values['name'],'actividad_id':id_actividadacambiar,'jefe_res_uid':valores_de_usuario[1],'usuario_cambiante':valores_de_usuario[0]})
                if values['secuencia']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET secuencia = "+str(values['secuencia'])+" "
                    else:
                        sql_yy2 += ", secuencia = "+str(values['secuencia'])+" "
                if values['um']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET um = '"+str(values['um'])+"' "
                    else:
                        sql_yy2 += ", um = '"+str(values['um'])+"' "
                if values['auxfrecuencia']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET auxfrecuencia = '"+str(values['auxfrecuencia'])+"' "
                    else:
                        sql_yy2 += ", auxfrecuencia = '"+str(values['auxfrecuencia'])+"' "
                if values['lun']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET lun = 't' "
                    else:
                        sql_yy2 += ", lun = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET lun = 'f' "
                    else:
                        sql_yy2 += ", lun = 'f' "                
                if values['mar']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET mar = 't' "
                    else:
                        sql_yy2 += ", mar = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET mar = 'f' "
                    else:
                        sql_yy2 += ", mar = 'f' "  
                if values['miercol']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET miercol = 't' "
                    else:
                        sql_yy2 += ", miercol = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET miercol = 'f' "
                    else:
                        sql_yy2 += ", miercol = 'f' "  
                if values['juev']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET juev = 't' "
                    else:
                        sql_yy2 += ", juev = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET juev = 'f' "
                    else:
                        sql_yy2 += ", juev = 'f' "  
                if values['viern']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET viern = 't' "
                    else:
                        sql_yy2 += ", viern = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET viern = 'f' "
                    else:
                        sql_yy2 += ", viern = 'f' "  
                if values['sabad']:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET sabad = 't' "
                    else:
                        sql_yy2 += ", sabad = 't' "
                else:
                    bandera = bandera + 1
                    if bandera == 1:
                        sql_yy2 += "SET sabad = 'f' "
                    else:
                        sql_yy2 += ", sabad = 'f' "  
                sql_yy2 += "WHERE id = "+str(id_actividadacambiar)
                crs_actividadespropias2.execute(sql_yy2)


        #Se modifica la actividad original esta no es importante y se elimina porque ha sido creada por el usuario
        res = super(activity, self).write(values)




        """

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
        """                   
        return res

    def get_id(self):
        cadenaaletoria = ""

        for n in range(32):
            aleatorio = random.choice(string.ascii_letters + string.digits)
            cadenaaletoria += aleatorio

        return cadenaaletoria