# -*- coding: utf-8 -*-
{
    'name': "HA",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "My Company",
    'website': "http://www.yourcompany.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/master/odoo/addons/base/module/module_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base'],

    # always loaded
    'data': [
        'security/user_groups.xml',
        'security/ir.model.access.csv',
        #'views/views.xml',
        'views/list_usuario_calificaciones.xml',
        'views/list_usuario_calificacionesp.xml',
        'views/ha.xml',
        'views/detallecalificaciones.xml',
        'views/detallecalificacionesprocesos.xml',
        #'views/combinado_evaluacion.xml',
        #'views/pusuarios_cargo.xml',
        #'views/usuariosacargo.xml',
        'views/configuracion.xml',
        'views/evaluacionjefeha.xml',
        'views/ev_test.xml',
        'views/pr_test.xml',
        'views/evaluacionprocesoha.xml',
        'views/userdefaultsections.xml',
        'views/auxiliaractividadescambiantes.xml',
        'views/fecha_corte.xml',
        'views/actividadesagregadasporelusuario.xml',
        #'views/evaluacion_dos_procs.xml',
        'views/menu_principal.xml',
        'data/defaultdata.xml',
        #'data/scheduler_data.xml',

    ],
    # only loaded in demonstration mode
    'demo': [
        #'demo/demo.xml',
    ],
    'css': ['/static/src/css/my_css.css'],
}