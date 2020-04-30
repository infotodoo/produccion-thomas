# -*- coding: utf-8 -*-
{
    'name': "Suprapak mrp",

    'summary': "Suprapak mrp",

    'description': "Suprapak mrp",

    'author': "Todoo SAS",
    'contributors': "Pablo Arcos pa@todoo.co, Oscar Bolaños ob@todoo.co",
    'website': "http://www.todoo.co",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/13.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Manufacturing',
    'version': '13.1',

    # any module necessary for this one to work correctly
    'depends': ['mrp_account_enterprise'],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/mrp_workcenter_view.xml',
        'views/mrp_cost_structure_template.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
        'demo/demo.xml',
    ],
}
