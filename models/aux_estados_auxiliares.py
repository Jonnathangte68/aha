from odoo import models, fields, api

import datetime
import pytz
import time
import psycopg2

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

    area_id = fields.Integer ()

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
                    print("Impresion de L")
                    print(lst[0][0])
                    print(lst[0][1])
                    datestring = datetime.datetime.strptime(str(lst[0][1]), "%Y-%m-%d %H:%M:%S.%f")
                    if datestring < datetime.datetime.now():
                        fModificada = datetime.datetime.now()

                        #Uso estos valores para calcular la siguiente fecha de corte para esa area
                        diaCorte = area_id.dia_corte
                        horaCorte = area_id.hora_corte
                        minutoCorte = area_id.minuto_corte
                        fCorteNueva = datetime.datetime.now().replace(hour=int(horaCorte),minute=int(minutoCorte))
                        fCorteNueva += datetime.timedelta(days=7)
                        #print(fCorteNueva)
                        crd = self.env.cr
                        crt = self.env.cr
                        cre = self.env.cr
                        #print("UPDATE aha_area SET fecha_corte = '"+str(fCorteNueva)+"' WHERE id = "+str(area_id.id))
                        crd.execute("UPDATE aha_area SET fecha_corte = '"+str(fCorteNueva)+"' WHERE id = "+str(area_id.id))
                        cre.execute("UPDATE aha_aux_estados_auxiliares SET activo = 'b' WHERE area_id = "+str(area_id.id))
                        mas_uno = int(lst[0][0]) + 1
                        crt.execute("INSERT INTO aha_aux_estados_auxiliares(ha_nro, fecha_corte, activo,area_id,fecha_creado) VALUES ("+str(mas_uno)+",'"+str(fCorteNueva)+"','a',"+str(area_id.id)+",current_timestamp)")
                else:
                    crt.execute("INSERT INTO aha_aux_estados_auxiliares(ha_nro, fecha_corte, activo,area_id,fecha_creado) VALUES ("+str('1')+",'"+str(datetime.datetime.now())+"','a',"+str(area_id.id)+",current_timestamp)")
                #tpla = lst[0]
                #ultimoId = tpla[0]
                #ultimoId = int(ultimoId)
                #ultimoId += 1
                #ultimaFech = tpla[1]
                #try:
                #    connect_str = "dbname='odoo3000replica' user='postgres' host='localhost' " + \
                #                  "password='agrovizion'"
                # use our connection values to establish a connection
                #conn = psycopg2.connect(connect_str)
                # create a psycopg2 cursor that can execute queries
                #cursor = conn.cursor()
                # create a new table with a single column called "name"
                #cursor.execute("SELECT fecha_corte FROM aha_aux_estados_auxiliares WHERE area_id = 1 and activo = 'a'")
                #rows = cursor.fetchall()
                #print(rows)
                #print(rows[0][0])
                #print(datetime.datetime.now())
                #print(rows[0][0] < datetime.datetime.now())
                #datestring = datetime.datetime.strptime(str(lst[1]), "%Y-%m-%d %H:%M:%S.%f")
                #print(type(datestring))
                #print(datestring)
                #fcomparacion = datetime.datetime.strftime(datestring, "%Y-%m-%d %H:%M:%S")
                #print(type(fcomparacion))
                """print(datestring < datetime.datetime.now())
                if datestring < datetime.datetime.now():
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
                """
                #print(fcomparacion)
                #print(datetime.datetime.now())

                """
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
                """
                #except Exception as e:
                #    print("Uh oh, can't connect. Invalid dbname, user or password?")
                #    print(e)
                #print(fechaCorteArea)
                #print("Fecha corte bruto")
                #print(area_id.fecha_corte)
                #the_time = time.strftime("%Y-%m-%d %H:%M:%S")
                #print("Aqui the time")
                #print(the_time)
                #fechacorte_cr = self.env.cr
                #print("SELECT fecha_corte FROM aha_aux_estados_auxiliares WHERE area_id = " + str(area_id.id) + " and activo = 'a'")
                #fechacorte_result = fechacorte_cr.execute("SELECT fecha_corte FROM aha_aux_estados_auxiliares WHERE area_id = " + str(area_id.id) + " and activo = 'a'")
                #resfechacorte = fechacorte_result.fetchone()
                #print(resfechacorte)
                #print(resfechacorte[0])
                #Fecha Actual
                #print(datetime.datetime.now())
                #tzz1='UTC'
                #tzz2='America/Tijuana'
                #ctzz1 = pytz.timezone(tzz1)
                #ctzz2 = pytz.timezone(tzz2)
                #trs = ctzz2.localize(datetime.datetime.strptime(the_time, "%Y-%m-%d %H:%M:%S")).astimezone(ctzz1)
                #print("no se si es timezone o fecha")
                #print(trs)
                #resultado_fecha_string = trs.strftime("%Y-%m-%d %H:%M:%S")
                #print("Aqui f")
                #print(fechaCorteArea)
                #print(resultado_fecha_string)
                #print("f actual")