# -*- coding: utf-8 -*-
{
    'name': "Ma Facturation",

    'summary': """
        Short (1 phrase/line) summary of the module's purpose, used as
        subtitle on modules listing or apps.openerp.com""",

    'description': """
        Long description of module's purpose
    """,

    'author': "ablaye ngom",
    'website': "https://www.ngomsrv.com",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/16.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Uncategorized',
    'version': '0.1',

    # any module necessary for this one to work correctly
    'depends': ['base','sale'],

    # always loaded
    'data': [
        'data/data_sequence.xml',
        'security/groups.xml',
        'security/ir.model.access.csv',
        'report/facture_avec_entete.xml',
        #'report/facture_sans_entete.xml',
        'views/views.xml',

    ],
    # only loaded in demonstration mode
    'demo': [

    ],
    'application': True,
    'auto_install': False,
}
