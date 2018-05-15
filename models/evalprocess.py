# -*- coding: utf-8 -*-

from odoo import models, fields, api
import random
import string

class evalprocess(models.Model):
    _name = 'aha.evalprocess'

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
        string='Verificar que la Ha este llena conforme al transcurso del dia',
    )

    criterio1commentario = fields.Text(
        string='Comentario',
    )

    criterio2check = fields.Boolean(
        string='Validar que las actividades con desviaciones (-) de la semana actual esten plasmados en las secciones de "Comentarios Relevantes" y "Acciones y Compromisos"',
    )

    criterio2commentario = fields.Text(
        string='Comentario',
    )

    criterio3check = fields.Boolean(
        string='Verificar el registro de una actividad aleatoria que se encuentre en HA para validar el entendimiento del registro',
    )

    criterio3commentario = fields.Text(
        string='Comentario',
    )

    criterio4check = fields.Boolean(
        string='Validar que HA cuente con firma de jefe inmediato de 3 semanas anteriores',
    )

    criterio4commentario = fields.Text(
        string='Comentario',
    )

    criterio5check = fields.Boolean(
        string='Validar que HA actual y de tres semanas anteriores se encuentre llena conforme al metodo (Sin mas de 3: espacios en blanco, N/A cuando no aplique, (-) cuando no se realice, Sumatoria de minutos y horas)',
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
        creado = super(evalprocess, self).create(values)
        cu = self.env.cr
        q = "update aha_ha set evalprocess_id = "+str(creado.id)+" WHERE id = "+str(creado.ha_id.id)
        cu.execute(q)

        """


        #Aqui calcular calificacion para procesos

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
        usuario_evaluado = self.env['aha.usuario'].search([('id','=',id_usuario)])
        if usuario_evaluado.calificacion_p:
            if usuario_evaluado.calificacion_p[:1] == cp[:1]:
                letra = usuario_evaluado.calificacion_p[:1]
                numero_aumentado = usuario_evaluado.calificacion_p[1:]
                enteroc = int(numero_aumentado)
                enteroc += 1
                #El aumento
                calif_total = letra + str(enteroc)
                usuario_evaluado.write({'calificacion_p':calif_total})
            else:
                calif_total = calificacion_particular + '1'
                usuario_evaluado.write({'calificacion_p':calif_total})
        else:
            usuario_evaluado.write({'calificacion_p':calificacion_particular + '1'})

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