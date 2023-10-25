# -*- coding: utf-8 -*-
{
    'name': 'Department Wise Product Report',
    'version': '1.0',
    'summary': 'Product Report module to meet supervisor requirement',
    'sequence': 3,
    'description': """
    Product Report
====================
""",
    'category': 'Report',
    'website': 'odoomates.com',
    'images': [],
    'depends': ['base','stock','sale','bahmni_sale'],
    'data': [
             'reports/pdf_action.xml',
             'reports/report_category_delivery_wizard_view.xml',
             'wizards/category_delivery_wizard_view.xml',
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
