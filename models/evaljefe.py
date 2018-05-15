# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string

class evaljefe(models.Model):
    _name = 'aha.evaljefe'

    #autogenerar este con el nombredelusuario y la semana de la hoja de actividad
    name = fields.Char(
        string='Evaluacion',
        default=lambda self: self.get_id()
    )

    #autocalculado en base a los criterios
    calificacion_general = fields.Char(
        string='Calificacion general',
        compute='_compute_calificacion',
        store=True
    )

    criterio1check = fields.Boolean(
        string='¿La HA se encuentra limpia y ordenada?',
    )

    criterio1commentario = fields.Text(
        string='Comentario',
    )

    criterio2check = fields.Boolean(
        string='¿La Ha se encuentra llena de acuerdo al método',
    )

    criterio2commentario = fields.Text(
        string='Comentario',
    )

    criterio3check = fields.Boolean(
        string='¿Los tiempos dedicados concuerdan con los resultados presentados?',
    )

    criterio3commentario = fields.Text(
        string='Comentario',
    )

    criterio4check = fields.Boolean(
        string='¿Validar si existen actividades claves sin revisar y cuestionar el porque?',
    )

    criterio4commentario = fields.Text(
        string='Comentario',
    )

    criterio5check = fields.Boolean(
        string='¿Validar si existen compromisos para las actividades no realizadas?',
    )

    criterio5commentario = fields.Text(
        string='Comentario',
    )

    ha_id = fields.Many2one(
        comodel_name='aha.ha',
        readonly=True
    )

    def get_id(self):
        cadenaaletoria = ""

        for n in range(32):
            aleatorio = random.choice(string.ascii_letters + string.digits)
            cadenaaletoria += aleatorio

        return cadenaaletoria

    @api.model
    def create(self, values):

        creado = super(evaljefe, self).create(values)
        cu = self.env.cr
        q = "update aha_ha set evaljefe_id = "+str(creado.id)+" WHERE id = "+str(creado.ha_id.id)
        cu.execute(q)

        """

        cp = ""
        a = 0
        b = 0 
        c = 0
        d = 0
        e = 0

        if values['criterio1check'] == True:
            a = 4
        if values['criterio2check'] == True:
            b = 6
        if values['criterio3check'] == True:
            c = 1
        if values['criterio4check'] == True:
            d = 9
        if values['criterio5check'] == True:
            e = 3

        suma = a+b+c+d+e
        if suma >= 22:
            cp = 'A'
        elif suma >= 10 and suma < 22:
            cp = 'B'
        else:
            cp = 'C'

        calificacion_particular = cp
        id_usuario = creado.ha_id.usuario_id.id
        
        if usuario_evaluado.calificacion_j:
            if usuario_evaluado.calificacion_j[:1] == cp[:1]:
                letra = usuario_evaluado.calificacion_j[:1]
                numero_aumentado = usuario_evaluado.calificacion_j[1:]
                enteroc = int(numero_aumentado)
                enteroc += 1
                #El aumento
                calif_total = letra + str(enteroc)
                print('Actualizo la calificacion')
                usuario_evaluado.write({'calificacion_j':calif_total})
            else:
                calif_total = calificacion_particular + '1'
                print('Actualizo y cambio la calificacion')
                usuario_evaluado.write({'calificacion_j':calif_total})
        else:
            print('Primera calificacion asignada')
            usuario_evaluado.write({'calificacion_j':calificacion_particular + '1'})

        """


        return creado

    @api.one
    @api.depends('criterio1check','criterio2check','criterio3check','criterio4check','criterio5check')
    def _compute_calificacion(self):
        a = 0
        b = 0 
        c = 0
        d = 0
        e = 0
        for criterio in self:
            if self.criterio1check == True:
                a = 4
            if self.criterio2check == True:
                b = 6
            if self.criterio3check == True:
                c = 1
            if self.criterio4check == True:
                d = 9
            if self.criterio5check == True:
                e = 3

        suma = a+b+c+d+e
        if suma >= 22:
            self.calificacion_general = 'A'
        elif suma >= 10 and suma < 22:
            self.calificacion_general = 'B'
        else:
            self.calificacion_general = 'C'