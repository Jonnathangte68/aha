# -*- coding: utf-8 -*-

from odoo import models, fields, api
import requests
import logging
import random
import string
import xlsxwriter
import datetime
from datetime import date
from io import BytesIO
import xlwt
from openerp.exceptions import except_orm, UserError
import math
import cgi
import pytz
import calendar
import time

_logger = logging.getLogger(__name__)

class ha(models.Model):
    _name = 'aha.ha'

    name = fields.Char(
        string='Hoja de actividad',
        required=False,
        default=lambda self: self.get_id()
    )

    # Tiene varias secciones 
    seccion_ids = fields.One2many(
        comodel_name='aha.section',
        inverse_name='ha_id',
        default=lambda self: self._set_default_sections(),
    )

    inicio_semana = fields.Datetime(
        string='Del:',
        #default=date.today(),
    )

    fin_semana = fields.Datetime(
        string='Hasta: ',
        default=date.today() + datetime.timedelta(days=6),
    )

    semana = fields.Integer(
        string='Semana',
    ) 

    # Pertenece a un usuario el que esta logeado
    usuario_id = fields.Many2one(
        comodel_name='aha.usuario',
        readonly=True
    )

    evaljefe_id = fields.Many2one(
        comodel_name='aha.evaljefe',
    )

    evalprocess_id = fields.Many2one(
        comodel_name='aha.evalprocess',
    )

    hausuario_id = fields.Integer(
        string='Id jefe',
        default=lambda self: self.get_user_id()
    )

    lunes_b = fields.Boolean(
        string='Lunes',
    )

    martes_b = fields.Boolean(
        string='Martes',
    )

    miercoles_b = fields.Boolean(
        string='Miercoles',
    )

    jueves_b = fields.Boolean(
        string='Jueves',
    )

    viernes_b = fields.Boolean(
        string='Viernes',
    )

    sabado_b = fields.Boolean(
        string='Sabado',
    )

    my_button = fields.Boolean('Ver limite para llenar hoja de actividad')

    evaluada = fields.Boolean(
        string='Si ya fue evaluada o no',
    )

    #ya_entro = fields.Char(default='no')

    #entro_nuevo = fields.Char(string='Bandera',default='n')

    contador = fields.Integer(string='Counter')

    #def __init__(self, pool, cr):
    #    counter_lunes = 0
    #    print('Counter Lunesssssssssssssssssssssssssssssssssssssssssssssss')

    def get_id(self):
        cadenaaletoria = ""

        for n in range(32):
            aleatorio = random.choice(string.ascii_letters + string.digits)
            cadenaaletoria += aleatorio

        return cadenaaletoria

    @api.model
    def create(self, values):
        """
        uss = self.env['aha.usuario'].search([('resuser_id.id','=',self.env.user.id)])
        ru_uid = uss.jefe_id.resuser_id
        values['usuario_id'] = uss.id
        values['hausuario_id'] = ru_uid
        creado = super(ha, self).create(values)
        for a in creado.seccion_ids:
            for b in a.activity_ids:
                if b.typo != 1:
                    self.env['aha.actividadesagregadasporelusuario'].create({
                        'name':b.name,
                        'um':b.um,
                        'frecuencia':b.frecuencia,
                        'lun':b.lun,
                        'mar':b.mar,
                        'miercol':b.miercol,
                        'juev':b.juev,
                        'viern':b.viern,
                        'sabad':b.sabad,
                        'section_id':b.section_id,
                        'section_name':a.name,
                        'typo':b.typo,
                        'actividad_id':b.name,
                        'usuario_id':creado.usuario_id,
                        'resuser_id':creado.usuario_id.resuser_id,
                        'ha_id':creado.name,
                        'secuencia':b.secuencia
                    })
        return creado
        """
        try:
            asigjefe_cr = self.env.cr
            asigjefe_cr.execute("SELECT jefe_uid FROM aha_usuario WHERE resuser_id = "+str(self.env.user.id))
            id_del_jefe = asigjefe_cr.fetchone()
            #print("Aqui este es el ID del jefe")
            #print(id_del_jefe[0])
            values['hausuario_id'] = id_del_jefe[0]
        except Exception as e:
            raise e
            #print(e)
        #print("Lo que lleva la Ha")
        #print(values)
        #print("Buscar ID de usuario")
        csor = self.env.cr
        csor.execute("SELECT id FROM aha_usuario WHERE resuser_id = "+str(self.env.user.id))
        id_buscado = csor.fetchone()
        #print("El id buscado es    " + str(id_buscado[0]))
        values['usuario_id'] = id_buscado[0]
        creado = super(ha, self).create(values)
        arrayactividadesagregar = []
        for seccions in creado.seccion_ids:
            for activids in seccions.activity_ids:
                #print("La actividad   " + str(activids.typo))
                if activids.typo == 0 or activids.typo == False:
                    #print("Entra al agregar una activ propia")
                    #print("La actividad  Detallesssss      typo   " + str(activids.typo) + " Nombre de actividad   " + str(activids.name)  + " seccion " + activids.section_id.name)
                    # Via sql
                    #print(self.env.user.id)
                    if not self.exist_in_my_own_activities(activids.name,activids.frecuencia,activids.um):
                        self.env['aha.actividadesagregadasporelusuario'].create({
                            'name':activids.name,
                            'um':activids.um,
                            'frecuencia':activids.frecuencia,
                            'lun':activids.lun,
                            'mar':activids.mar,
                            'miercol':activids.miercol,
                            'juev':activids.juev,
                            'viern':activids.viern,
                            'sabad':activids.sabad,
                            'section_id':activids.section_id,
                            'section_name':seccions.name,
                            'typo':activids.typo,
                            'actividad_id':activids.name,
                            'usuario_id':creado.usuario_id,
                            'resuser_id':self.env.user.id,
                            'ha_id':creado.name,
                            'secuencia':activids.secuencia
                        })
        return creado

    @api.multi
    def print_ha(self):
        c = self.env.cr
        sql1 = "SELECT login FROM res_users WHERE res_users.id = '"+str(self.env.user.id)+"'"
        c.execute(sql1)
        resultado_usuario = c.fetchone()
        cuh = self.env.cr
        sql134 = "select name from res_users inner join aha_usuario on aha_usuario.resuser_id = res_users.id where res_users.id = '"+str(self.env.user.id)+"'"
        cuh.execute(sql134)
        nameee_usuario = cuh.fetchone()
        #print("Aquiiiiiiiiiiiiiiiiiiiiiiiiiii ->      "+str(nameee_usuario[0]))
        usuario_id = nameee_usuario[0]
        #raise nameee_usuario
        #print('Acaaaaaaaaaaaaaa el valor del cursor')
        #print(resultado_usuario[0])

        #select aha_area.name from aha_area inner join aha_usuario on aha_usuario.area_id = aha_area.id where aha_usuario.id = 4
        cu = self.env.cr
        sql2 = "SELECT aha_area.name,fecha_corte FROM aha_area INNER JOIN aha_usuario ON aha_usuario.area_id = aha_area.id WHERE aha_usuario.resuser_id = "+str(self.env.user.id)
        cu.execute(sql2)
        #if not cu:
        try:
            resultado_area = cu.fetchone()
        except Exception as e:
            raise e

        html_escape_table = {
            "&": "&amp;",
            '"': "&quot;",
            "'": "&apos;",
            "/": "&sol;",
            ">": "&gt;",
            "<": "&lt;",
            "-": "&ndash;",
            '!': '&excl;',
            '#': '&num;',
            '$': '&dollar;',
            '%': '&percnt;',
            '(': '&lpar;',
            ')': '&rpar;',
            '*': '&ast;',
            '.': '&period;',
            ',': '&comma;',
            ':': '&colon;',
            '?': '&quest;',
            '@': '&commat;',
            '^': '&Hat;',
            '_': '&lowbar;',
            '|': '&vert; ',
            'é': '&eacute;',
            'ó': '&oacute;',
            'á': '&aacute;',
            'í': '&iacute;',
            'ú': '&uacute;',
            ' ': '&nbsp;',
            'Ñ':'&Ntilde',
            'ñ':'&ntilde',  
        }
        """
        print("Aquiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiiii")
        print(self.inicio_semana)
        print(self.fin_semana)
        print(type(self.inicio_semana))
        print(type(self.fin_semana))
        f111 = datetime.datetime.strptime(self.inicio_semana, "%Y-%m-%d %H:%M:%S")
        print(f111)
        current111_tz2='UTC'
        target111_tz2='America/Tijuana'
        current111_tz2 = pytz.timezone(current111_tz2)
        target111_tz2 = pytz.timezone(target111_tz2)
        target111_dt2 = current111_tz2.localize(datetime.datetime.strptime(f111, "%Y-%m-%d %H:%M:%S")).astimezone(target111_tz2)
        print(target111_dt2)
        """
        #stringDate2222 = target222_dt2.strftime("%Y-%m-%d %H:%M:%S")

        ha_id = "".join(html_escape_table.get(c,c) for c in self.name)
        #print(ha_id)
        sem = self.semana
        #desdeel = self.inicio_semana[8:10]
        #hastael = self.fin_semana[8:10]
        #print('Desdeeeeeeeeeeeeeeee elllllllllllllllllllllllllllllll')
        #print(desdeel)
        #print('Dia menos')
        #desdeel = int(desdeel)-1
        #desdeel = int(desdeel)
        #desdeel = int(30)
        #f111 = self.inicio_semana.strftime("%Y-%m-%d %H:%M:%S")
        """
        auxf111 = self.inicio_semana
        f111 = datetime.strptime(auxf111, "%Y-%m-%d %H:%M:%S")
        current111_tz2='UTC'
        target111_tz2='America/Tijuana'
        current111_tz2 = pytz.timezone(current111_tz2)
        target111_tz2 = pytz.timezone(target111_tz2)
        target111_dt2 = current111_tz2.localize(datetime.datetime.strptime(f111, "%Y-%m-%d %H:%M:%S")).astimezone(target111_tz2)
        stringDate2111 = target111_dt2.strftime("%Y-%m-%d %H:%M:%S")
        print("Fecha correctaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(stringDate2111)
        auxf222 = self.inicio_semana
        f222 = datetime.strptime(auxf222, "%Y-%m-%d %H:%M:%S")
        current222_tz2='UTC'
        target222_tz2='America/Tijuana'
        current222_tz2 = pytz.timezone(current222_tz2)
        target222_tz2 = pytz.timezone(target222_tz2)
        target222_dt2 = current222_tz2.localize(datetime.datetime.strptime(f222, "%Y-%m-%d %H:%M:%S")).astimezone(target222_tz2)
        stringDate2222 = target222_dt2.strftime("%Y-%m-%d %H:%M:%S")
        print("****************** Fecha correctaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
        print(stringDate2222)
        """
        #f111 = datetime.datetime.strptime(stringDate2111, '%Y-%m-%d %H:%M:%S')
        #print(desdeel)
        #print('----------------------- INICIO SEMANA -----------------------------------')
        #print(self.inicio_semana)
        #print('Hastaaaaaaaaaaaaaaaaaaaaaaaa ellllllllllllllllllllllllllll')
        #print(hastael)
        #hastael = int(hastael)-1
        #print(hastael)
        #print('------------------------ FIN SEMANA --------------------------------------')
        #print(self.fin_semana)

        current222_tz2='UTC'
        target222_tz2='America/Tijuana'
        current222_tz2 = pytz.timezone(current222_tz2)
        target222_tz2 = pytz.timezone(target222_tz2)
        target222_dt2_primera_fecha = current222_tz2.localize(datetime.datetime.strptime(self.inicio_semana, "%Y-%m-%d %H:%M:%S")).astimezone(target222_tz2)
        target222_dt2 = current222_tz2.localize(datetime.datetime.strptime(self.fin_semana, "%Y-%m-%d %H:%M:%S")).astimezone(target222_tz2)
        stringDate2222 = target222_dt2.strftime("%Y-%m-%d %H:%M:%S")
        stringDate1111 = target222_dt2_primera_fecha.strftime("%Y-%m-%d %H:%M:%S")

        #print("inicio semana " + stringDate1111)
        #print("Cortado " + stringDate1111[8:10])
        #print("fin semana " + stringDate2222)
        #print("Cortado " + stringDate2222[8:10])


        desdeel = int(stringDate1111[8:10])
        hastael = int(stringDate2222[8:10])
        mes_entero_remplaz = stringDate1111[5:7]
        #mes_entero_remplaz = int(stringDate1111[5:7])
        mes_entero_remplaz2 = stringDate2222[5:7]
        #mes_entero_remplaz = int(stringDate2222[5:7])
        #print("Aqui mesesssssssssssssssssssssssssssssssss")


        #usuario_id = "".join(html_escape_table.get(c,c) for c in resultado_usuario[0])
        


        #print(usuario_id)
        fechaHoja = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        current_tz2='UTC'
        target_tz2='America/Tijuana'
        current_tz2 = pytz.timezone(current_tz2)
        target_tz2 = pytz.timezone(target_tz2)
        target_dt2 = current_tz2.localize(datetime.datetime.strptime(fechaHoja, "%Y-%m-%d %H:%M:%S")).astimezone(target_tz2)
        stringDate2 = target_dt2.strftime("%Y-%m-%d %H:%M:%S")
        fechaHoja = datetime.datetime.strptime(stringDate2, '%Y-%m-%d %H:%M:%S')
        if cu:
            if resultado_area:
                area_id = "".join(html_escape_table.get(c,c) for c in resultado_area[0]) #resultado_area[0] if not resultado_area else ""
                #current_tz='UTC'
                #target_tz='America/Tijuana'
                #current_tz = pytz.timezone(current_tz)
                #target_tz = pytz.timezone(target_tz)
                #target_dt = current_tz.localize(datetime.datetime.strptime(resultado_area[1], "%Y-%m-%d %H:%M:%S")).astimezone(target_tz)
                #stringDate = target_dt.strftime("%Y-%m-%d %H:%M:%S")
                #fechaArea = datetime.datetime.strptime(stringDate, '%Y-%m-%d %H:%M:%S')
                #print('ACaaaaaaaaaaaaaaaa valoresss')
                #print(stringDate)
                #print(fechaArea)
                #subfecha = target_dt.strftime("%Y-%m-%d %H:%M:%S")
                #fechaArea = datetime.datetime.strptime(resultado_area[1], "%Y-%m-%d %H:%M:%S")
                #if fechaHoja < fechaArea:
                #    condiciontiempo = '1'
                #else:
                #    condiciontiempo = '0'
        else:
            area_id = 'NA'

        mes_uno = mes_entero_remplaz
        mes_dos = mes_entero_remplaz2

        if mes_uno == '01':
            mes_uno = 'Ene'
        elif mes_uno == '02':
            mes_uno = 'Feb'
        elif mes_uno == '03':
            mes_uno = 'Mar'
        elif mes_uno == '04':
            mes_uno = 'Abr'
        elif mes_uno == '05':
            mes_uno = 'May'
        elif mes_uno == '06':
            mes_uno = 'Jun'
        elif mes_uno == '07':
            mes_uno = 'Jul'
        elif mes_uno == '08':
            mes_uno = 'Ago'
        elif mes_uno == '09':
            mes_uno = 'Sep' 
        elif mes_uno == '10':
            mes_uno = 'Oct'
        elif mes_uno == '11':
            mes_uno = 'Nov'
        else:
            mes_uno = 'Dic'

        if mes_dos == '01':
            mes_dos = 'Ene'
        elif mes_dos == '02':
            mes_dos = 'Feb'
        elif mes_dos == '03':
            mes_dos = 'Mar'
        elif mes_dos == '04':
            mes_dos = 'Abr'
        elif mes_dos == '05':
            mes_dos = 'May'
        elif mes_dos == '06':
            mes_dos = 'Jun'
        elif mes_dos == '07':
            mes_dos = 'Jul'
        elif mes_dos == '08':
            mes_dos = 'Ago'
        elif mes_dos == '09':
            mes_dos = 'Sep' 
        elif mes_dos == '10':
            mes_dos = 'Oct'
        elif mes_dos == '11':
            mes_dos = 'Nov'
        else:
            mes_uno = 'Dic'



        """ Ejemplo este recorrido me trae       ** titulo, lista **
        secciones = []
        for sec in self.seccion_ids:
            print('seccion')
            secciones.append("".join(html_escape_table.get(c,c) for c in sec.name))
            secciones.append(sec.activity_ids)
        print(secciones)
        """

        usxareaId = self.env['aha.usuario'].search([('resuser_id','=',self.env.user.id)]).area_id.id
        condiciontiempo = '0'
        cursor_condicion = self.env.cr
        #print("SELECT ha_nro FROM aha_aux_estados_auxiliares WHERE area_id = '"+str(usxareaId)+"' AND activo = 'a'")
        cursor_condicion.execute("SELECT ha_nro FROM aha_aux_estados_auxiliares WHERE area_id = '"+str(usxareaId)+"' AND activo = 'a'")
        semana_correcta = cursor_condicion.fetchone()
        #print('AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII LA SEMANAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAA')
        #print(semana_correcta[0])
        #print(semana_correcta)
        #print(semana_correcta[0])
        if semana_correcta:
            if sem == semana_correcta[0]:
                #Esta en la semana correspondiente
                condiciontiempo = '1'

        secciones = []
        for sec in self.seccion_ids:
            #print('seccion')
            activitycounter = 1
            secciones.append("".join(html_escape_table.get(c,c) for c in sec.name))
            arrlocal = []
            for ac in sec.activity_ids:
                ll = []
                ll.append(ac.secuencia)
                ll.append("".join(html_escape_table.get(c,c) for c in ac.name[:61]) if ac.name else " ")
                #print("".join(html_escape_table.get(c,c) for c in ac.name))
                ll.append("".join(html_escape_table.get(c,c) for c in ac.um) if ac.um else " ")
                #print("AQUIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIIII")
                #print(ac.frecuencia)
                #print("".join(html_escape_table.get(c,c) for c in ac.um))
                if ac.frecuencia:
                    ll.append("".join(html_escape_table.get(c,c) for c in ac.frecuencia))
                else:
                    ll.append('')
                if ac.auxfrecuencia:
                    ll.append("".join(html_escape_table.get(c,c) for c in ac.auxfrecuencia))
                else:
                    ll.append('')
                if self.contador > 6:
                    if self.lunes_b:
                        ll.append(False)
                    else:
                        ll.append(ac.lun)
                else:
                    ll.append(ac.lun)
                if self.contador > 6:
                    if self.martes_b:
                        ll.append(False)
                    else:
                        ll.append(ac.mar)
                else:
                    ll.append(ac.mar)
                if self.contador > 6:
                    if self.miercoles_b:
                        ll.append(False)
                    else:
                        ll.append(ac.miercol)
                else:
                    ll.append(ac.miercol)
                if self.contador > 6:
                    if self.jueves_b:
                        ll.append(False)
                    else:
                        ll.append(ac.juev)
                else:
                    ll.append(ac.juev)
                if self.contador > 6:
                    if self.viernes_b:
                        ll.append(False)
                    else:
                        ll.append(ac.viern)
                else:
                    ll.append(ac.viern)
                if self.contador > 6:
                    if self.sabado_b:
                        ll.append(False)
                    else:
                        ll.append(ac.sabad)
                else:
                    ll.append(ac.sabad)
                arrlocal.append(ll)
                activitycounter += 1
                ll = []
            arreglo_ordenado = sorted(arrlocal, key=lambda actividad: actividad[0]) 
            #print('Aqui impresion de los resultados ordenados')
            #print(arreglo_ordenado)
            secciones.append(arreglo_ordenado)
            arrlocal = []
        #print(secciones)
        
        #Puede dar error sino hay rol para el usuario
        # Traer el Rol
        rolee = "".join(html_escape_table.get(c,c) for c in self.env['aha.usuario'].search([('resuser_id','=',self.env.user.id)]).rol_id.name)


        return {
            'type' : 'ir.actions.act_url',
            'url': '/impresionexcel/impresionexcel/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s/%s' % (ha_id,sem,desdeel,hastael,secciones,usuario_id,area_id,mes_uno,mes_dos,condiciontiempo,rolee),
            'target': 'self',
        }

    @api.multi
    def evpr(self):

        return {
            'name': 'Evalaucion de la Hoja de Actividad',
            'view_mode': 'form',
            'view_id': self.env.ref('aha.formulario_evaluacion_jefe_ha').id,
            'view_type': 'form',
            'res_model': 'aha.evaljefe',
            'type': 'ir.actions.act_window',
            'target': 'self',
            'context': {
                'default_ha_id': self.id,
            }
        }

    @api.multi
    def evaluar_ha(self):

        return {
            'name': 'Evalaucion de la Hoja de Actividad',
            'view_mode': 'form',
            'view_id': self.env.ref('aha.formulario_evaluacion_proccess_ha').id,
            'view_type': 'form',
            'res_model': 'aha.evalprocess',
            'type': 'ir.actions.act_window',
            'target': 'self',
            'context': {
                'default_ha_id': self.id,
            }
        }
        
    @api.multi
    @api.onchange('my_button')
    def onchange_my_button(self):
        warning_msg = ""

        for record in self:
            fc = self.get_fecha_corte(self.env.user.id)
            #print(fc)
            if fc == "":
                #raise except_orm(('Notificacion!'),('Fecha de corte no asignada todavia'))
                warning_msg = "Fecha de corte no asignada todavia"
            else:
                #current_tz='UTC'
                #target_tz='America/Tijuana'
                #current_tz = pytz.timezone(current_tz)
                #target_tz = pytz.timezone(target_tz)
                if fc:
                #    target_dt = current_tz.localize(datetime.datetime.strptime(fc, "%Y-%m-%d %H:%M:%S")).astimezone(target_tz)
                #    subfecha = target_dt.strftime("%Y-%m-%d %H:%M:%S")
                    #raise except_orm(('Notificacion!'),('Tiene hasta el '+str(subfecha)+' para llenar su hoja de actividad'))
                    #Como estaba
                    #warning_msg = "Tiene hasta el "+str(subfecha)+" para llenar su hoja de actividad"
                    #Nuevo metodo
                    warning_msg = "Tiene hasta el dia "+str(fc)+" para llenar su hoja de actividad"                    
                else:
                    #raise except_orm(('Notificacion!'),('No se han asignado fechas de corte para las areas'))
                    warning_msg = "No se han asignado fechas de corte para las areas"
        warning = {
            'title': 'Fecha Limite para su Ha!',
            'message': warning_msg,
        }
        return {'warning': warning}

    def check_existance(self, context=None):
        search_ids = self.search([('inicio_semana', '=', self.inicio_semana),('fin_semana', '=' , self.fin_semana),('usuario_id', '=' , self.env.user.id)])
        res = True
        if len(search_ids) > 1:
            res = False
        return res

    #_constraints = [(check_existance,'Su Ha ya se encuentra registrada, saludos!', ['inicio_semana','fin_semana','usuario_id'])]

    def _set_default_sections(self):
        #print('SET DEFAULT SECTIONSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSSS')


        # Primero lo primera borrar las actividades anteriores

        cursor_loco = self.env.cr
        cursor_loco.execute("DELETE FROM AHA_ACTIVITY WHERE create_uid = "+str(self.env.user.id))


        #cursor_noqueremosveanrepetidas = self.env.cr
        #cursor_noqueremosveanrepetidas.execute("DELETE FROM AHA_ACTIVIDADESAGREGADASPORELUSUARIO WHERE id IN (SELECT id FROM (SELECT id,ROW_NUMBER() OVER( PARTITION BY name ORDER BY  id DESC) AS row_num FROM AHA_ACTIVIDADESAGREGADASPORELUSUARIO ) t WHERE t.row_num > 1 AND create_uid = "+str(self.env.user.id)+")")

        # Ahora si todo el desmadre


        resultadoTot = self.env['aha.section']
        if len(self.env['aha.usuario'].search([])) > 0:
            usuario = self.env['aha.usuario'].search([('resuser_id', '=', self.env.user.id)])
            for i in usuario:
                rol = usuario.rol_id
                for k in rol:
                    for z in k.tipoha_id:
                        #print(z.section_ids)
                        if len(z.section_ids) > 0:
                            for sec in z.section_ids:
                                seccion = self.env['aha.section'].sudo().create({
                                    'name':sec.name,
                                })
                                if len(sec.activity_ids) > 0:  
                                    for atv in sec.activity_ids:  
                                        #print(" Valores que dan error : --> name"+ str(atv.name) + "aux frecuencia" +str(atv.auxfrecuencia))                               
                                        if atv.typo:    
                                            activity = self.env['aha.activity'].sudo().create({
                                                'name':atv.name,
                                                'um':atv.um,
                                                'frecuencia':atv.frecuencia,
                                                'secuencia':atv.secuencia,
                                                'lun':atv.lun,
                                                'mar':atv.mar,
                                                'miercol':atv.miercol,
                                                'juev':atv.juev,
                                                'viern':atv.viern,
                                                'sabad':atv.sabad,
                                                'section_id':seccion.id,
                                                'typo':atv.typo,
                                                'cambio':atv.cambio,
                                                'aaa':atv.aaa,
                                                'auxfrecuencia':atv.auxfrecuencia
                                            })
                                auxactividadesagregadas = []
                                actpropiass = self.env['aha.actividadesagregadasporelusuario'].search([('usuario_id','=',usuario.id)])
                                #print(actpropiass)
                                #print(usuario.id)
                                for avpropia in actpropiass:
                                    #print('Aquiiiiiiiiiiiiiiiiiiiiiiiiiii nombressssssssssss comparaaaaaaaaaaaaaaaaaaaaaaaaaaaa')
                                    #print(avpropia.section_name)
                                    #print(sec.name)
                                    #print('Usuario id: '+str(usuario.id))
                                    #print('Usuario id: '+str(avpropia.usuario_id))
                                    #print('Nombre de la Actividad: '+str(avpropia.name))
                                    if avpropia.section_name == sec.name:
                                        if avpropia.name not in auxactividadesagregadas:
                                            acty = self.env['aha.activity'].create({
                                                'name':avpropia.name,
                                                'um':avpropia.um,
                                                'frecuencia':avpropia.frecuencia,
                                                'secuencia':avpropia.secuencia,
                                                'lun':avpropia.lun,
                                                'mar':avpropia.mar,
                                                'miercol':avpropia.miercol,
                                                'juev':avpropia.juev,
                                                'viern':avpropia.viern,
                                                'sabad':avpropia.sabad,
                                                'section_id':seccion.id,
                                                'typo':avpropia.typo,
                                                'cambio':avpropia.cambio,
                                                'aaa':avpropia.aaa,
                                                'auxfrecuencia':avpropia.auxfrecuencia
                                            })
                                            auxactividadesagregadas.append(acty.name)
                                resultadoTot = resultadoTot + seccion
                            return resultadoTot
                        else:
                            return []
        

    def get_fecha_corte(self, usuario):
        a = self.env['aha.usuario'].search([])
        for i in a:
            if i.resuser_id.id == self.env.user.id:
                self.env['aha.area'].search([])
                jj = self.env['aha.area'].search([])
                for a in jj:
                    if a.id == i.area_id.id:
                        dia = ""
                        cursor_mine_mine = self.env.cr
                        cursor_mine_mine.execute("select fecha_corte from aha_aux_estados_auxiliares where area_id = "+str(a.id)+" and activo = 'a'")
                        mifetchdate = cursor_mine_mine.fetchone()
                        #print("Aqui mi fetch dateeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
                        #print(mifetchdate[0])
                        #dia_entero = datetime.datetime.strptime(i.area_id.fecha_corte, "%Y-%m-%d %H:%M:%S")#.isoweekday()
                        current_tz='UTC'
                        target_tz='America/Tijuana'
                        current_tz = pytz.timezone(current_tz)
                        target_tz = pytz.timezone(target_tz)
                        dia_entero = current_tz.localize(datetime.datetime.strptime(mifetchdate[0], "%Y-%m-%d %H:%M:%S.%f")).astimezone(target_tz).isoweekday()
                        #print("En get fecha corte    ---- >   el dia "+str(i.area_id.fecha_corte))
                        #print('Datetime correcto!')
                        #print(dia_entero)
                        if dia_entero == 1:
                            dia = "Lunes"
                        elif dia_entero == 2:
                            dia = "Martes"
                        elif dia_entero == 3:
                            dia = "Miercoles"
                        elif dia_entero == 4:
                            dia = "Jueves"
                        elif dia_entero == 5:
                            dia = "Viernes"
                        else:
                            dia = "Sabado"
                        return dia
        fc = ""
        return fc

    @api.multi
    @api.onchange('inicio_semana', 'fin_semana')
    def validar_inicio(self): 
        #print('valida')
        if self.inicio_semana and self.fin_semana:
            if self.inicio_semana > self.fin_semana:
                self.inicio_semana = date.today()
                self.fin_semana = date.today() + datetime.timedelta(days=1)

    @api.multi
    def get_user_id(self):
        usuario_id = self.env['aha.usuario'].search([('resuser_id','=',self.env.user.id)]).jefe_id.id
        return usuario_id

    @api.multi
    def evaluar_ha_procesos(self):
        #print('prueba procesos')
        return {
            'name': 'Evalaucion de la Hoja de Actividad',
            'view_mode': 'form',
            'view_id': self.env.ref('aha.formulario_evaluacion_proccess_ha').id,
            'view_type': 'form',
            'res_model': 'aha.evalprocess',
            'type': 'ir.actions.act_window',
            'target': 'self',
            'context': {
                'default_ha_id': self.id,
            }
        }

    @api.multi
    def evaluar_ha_jefe(self):
        #print('prueba jefe')
        return {
            'name': 'Evalaucion de la Hoja de Actividad',
            'view_mode': 'form',
            'view_id': self.env.ref('aha.formulario_evaluacion_jefe_ha').id,
            'view_type': 'form',
            'res_model': 'aha.evaljefe',
            'type': 'ir.actions.act_window',
            'target': 'self',
            'context': {
                'default_ha_id': self.id,
            }
        }

    @api.multi
    def test_act(self):
        #print('PRUEBAAAAAAAAAAAAAAAAAAAAA DE MI METODOOOOOOOOOOOOO ACTIIONNNNNN SERVERRRRRRRRRRRRRRRRRRRRRRR')
        var1 = 'test'
        var2 = 'test 2'
        return {
            'type' : 'ir.actions.act_url',
            #'url': '/impresionexcel/evaluate/%s/%s' % (var1,var2),
            'url': 'http://www.google.com/',
            'target': 'self',
        }
    
    # Si existe una actividad propias con el mismo nombre, la misma frecuencia y la misma unidad de medida retorna FALSE caso contrario retorna TRUE
    def exist_in_my_own_activities(self,activity_name, activity_frecuencia, activity_um):
        try:
            for avpropia in self.env['aha.actividadesagregadasporelusuario'].search([('resuser_id','=',self.env.user.id)]):
                if avpropia.name == activity_name and avpropia.frecuencia == activity_frecuencia and avpropia.um == activity_um:
                    return True
            return False
        except Exception as e:
            return False

    @api.multi
    @api.onchange('lunes_b')
    def onchange_lunes_b(self):
        if self.lunes_b:
            self.lunes_change_db('s')
        else:
            self.lunes_change_db('n')

    @api.multi
    @api.onchange('martes_b')
    def onchange_martes_b(self):
        if self.martes_b:
            self.lunes_change_db('','s')
        else:
            self.lunes_change_db('','n')

    @api.multi
    @api.onchange('miercoles_b')
    def onchange_miercoles_b(self):            
        if self.miercoles_b:
            self.lunes_change_db('','','s')
        else:
            self.lunes_change_db('','','n')

    @api.multi
    @api.onchange('jueves_b')
    def onchange_jueves_b(self):  
        if self.jueves_b:
            self.lunes_change_db('','','','s')
        else:
            self.lunes_change_db('','','','n')

    @api.multi
    @api.onchange('viernes_b')
    def onchange_viernes_b(self):  
        if self.viernes_b:
            self.lunes_change_db('','','','','s')
        else:
            self.lunes_change_db('','','','','n')

    @api.multi
    @api.onchange('sabado_b')
    def onchange_sabado_b(self):  
        if self.sabado_b:
            self.lunes_change_db('','','','','','s')
        else:
            self.lunes_change_db('','','','','','n')

    def lunes_change_db(self, lunes = '', martes = '', miercoles = '', jueves = '', viernes = '', sabado = ''):
        #print(self.entro_nuevo)isinstance(i,list):
        #Falta: Recorrer todas las actividades propias y actualizar su dia bloqueado
        self.contador += 1
        """
        if self.contador > 6:
            if lunes == 's':
                print(self.seccion_ids)
                self.env.cr.execute("UPDATE AHA_ACTIVITY SET lun = 'FALSE' WHERE create_uid = "+str(self.env.user.id)+";UPDATE AHA_ACTIVIDADESAGREGADASPORELUSUARIO SET lun = 'FALSE' WHERE create_uid = "+str(self.env.user.id))
                self.env.cr.commit()
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        actividad.lun = False
                        print('Aqui actividadd')
                        print(actividad)
                        print(actividad.lun)
            elif martes == 's':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif miercoles == 's':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif jueves == 's':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif viernes == 's':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif sabado == 's':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif lunes == 'n':
                self.env.cr.execute("UPDATE AHA_ACTIVITY SET lun = 'TRUE' WHERE create_uid = "+str(self.env.user.id)+";UPDATE AHA_ACTIVIDADESAGREGADASPORELUSUARIO SET lun = 'TRUE' WHERE create_uid = "+str(self.env.user.id))
                self.env.cr.commit()
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        actividad.lun = True
                        print('Aqui actividadd')
                        print(actividad)
                        print(actividad.lun)
            elif martes == 'n':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif miercoles == 'n':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif jueves == 'n':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif viernes == 'n':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
            elif sabado == 'n':
                for grupo_actividades in self.seccion_ids:
                    for actividad in grupo_actividades.activity_ids:
                        print(actividad)
        """