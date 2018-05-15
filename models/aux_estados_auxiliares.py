from odoo import models, fields, api

import datetime

#Import logger
import logging
#Get the logger
_logger = logging.getLogger(__name__)

class aux_estados_auxiliares(models.Model):
    _name = 'aha.aux_estados_auxiliares'

    ha_nro = fields.Integer(
        string='Numero de ha',
    )

    fecha_corte = fields.Datetime(
        string='Fecha de Corte',
    )

    fecha_creado = fields.Datetime(
        string='Fecha de cambio',
    )

    activo = fields.Char(
        string='Activo',
    )

    #This function is called when the scheduler goes off
    def process_demo_scheduler_queue(self):
        #print('test')
        #_logger.info('Test Cron test')
        #Para tener el ultimo Id de la tabla y la ultima fecha de corte

        #user = self.env['aha.usuario'].search([('resuser_id','=',self.env.user.id)])
        #Como debe ser es como esta arriba, debajo para probar
        #user = self.env['aha.usuario'].search([('resuser_id','=',19)])

        #Despues buscar area y del area se tiene el dia de corte, la hora de corte y el minuto de corte

        #d = datetime.datetime.strptime(ultimaFech,'%Y-%m-%d %H:%M:%S.%f')
            

        for area_id in self.env['aha.area'].search([]):

            if area_id.fecha_corte:

                cr = self.env.cr
                #crd = self.env.cr
                cr.execute("SELECT ha_nro,fecha_corte FROM aha_aux_estados_auxiliares where area_id = "+str(area_id.id)+" order by fecha_corte desc limit 1")
                lst = cr.fetchall()
                if lst:
                    tpla = lst[0]
                    ultimoId = tpla[0]
                    ultimoId = int(ultimoId)
                    ultimoId += 1
                    ultimaFech = tpla[1]
                #else:
                #    if area_id.dia_corte == 'lunes':
                #        fCorteInicio = datetime.datetime.strptime('2018-01-01 10:00:00',"%Y-%m-%d %H:%M:%S")
                #    elif area_id.dia_corte == 'martes':
                #        fCorteInicio = datetime.datetime.strptime('2018-01-02 10:00:00',"%Y-%m-%d %H:%M:%S")
                #    elif area_id.dia_corte == 'miercoles':
                #        fCorteInicio = datetime.datetime.strptime('2018-01-03 10:00:00',"%Y-%m-%d %H:%M:%S")
                #    elif area_id.dia_corte == 'jueves':
                #        fCorteInicio = datetime.datetime.strptime('2018-01-04 10:00:00',"%Y-%m-%d %H:%M:%S")
                #    elif area_id.dia_corte == 'viernes':
                #        fCorteInicio = datetime.datetime.strptime('2018-01-05 10:00:00',"%Y-%m-%d %H:%M:%S")
                #    elif area_id.dia_corte == 'sabado':
                #        fCorteInicio = datetime.datetime.strptime('2018-01-06 10:00:00',"%Y-%m-%d %H:%M:%S")

                fechaCorteArea = datetime.datetime.strptime(area_id.fecha_corte,"%Y-%m-%d %H:%M:%S")

                #print(fechaCorteArea)

                #Fecha Actual
                #print(datetime.datetime.now())

                if fechaCorteArea < datetime.datetime.now():
                    print('Actualizar fecha corte de area para que sea mayor y hacer operaciones en la tabla de estados')

                    fModificada = datetime.datetime.now()

                    #Uso estos valores para calcular la siguiente fecha de corte para esa area
                    diaCorte = area_id.dia_corte
                    horaCorte = area_id.hora_corte
                    minutoCorte = area_id.minuto_corte

                    #fModificada = fModificada + datetime.timedelta(days=7)
                    #fModificada.replace(hour=11, minute=59)
                    fCorteNueva = datetime.datetime.now().replace(hour=int(horaCorte),minute=int(minutoCorte))
                    fCorteNueva += datetime.timedelta(days=7)
                    #print(fCorteNueva)
                    crd = self.env.cr
                    crt = self.env.cr
                    cre = self.env.cr
                    #print("UPDATE aha_area SET fecha_corte = '"+str(fCorteNueva)+"' WHERE id = "+str(area_id.id))
                    crd.execute("UPDATE aha_area SET fecha_corte = '"+str(fCorteNueva)+"' WHERE id = "+str(area_id.id))
                    cre.execute("UPDATE aha_aux_estados_auxiliares SET activo = 'b' WHERE area_id = "+str(area_id.id))
                    if lst:
                        crt.execute("INSERT INTO aha_aux_estados_auxiliares(ha_nro, fecha_corte, activo,area_id,fecha_creado) VALUES ("+str(ultimoId)+",'"+str(fCorteNueva)+"','a',"+str(area_id.id)+",current_timestamp)")
                    else:
                        crt.execute("INSERT INTO aha_aux_estados_auxiliares(ha_nro, fecha_corte, activo,area_id,fecha_creado) VALUES ("+str('1')+",'"+str(fCorteNueva)+"','a',"+str(area_id.id)+",current_timestamp)")