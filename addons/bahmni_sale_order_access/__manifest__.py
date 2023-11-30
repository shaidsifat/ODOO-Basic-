# -*- coding: utf-8 -*-
{
    'name': 'Bahmni SaleOrder Access',
    'version': '1.0',
    'summary': 'Custom  SaleOrder Access module to meet bahmni requirement',
    'sequence': 8,
    'description': """
Bahmni  SaleOrder Access
====================
""",
    'category': 'Sales',
    'website': '',
    'images': [],
    'depends': ['base','sale', 'sale_stock','sales_team', 'bahmni_account','point_of_sale','account','web','report'],
    'data': [
              'security/security_groups.xml',
              'security/ir.model.access.csv',

             ],
    'demo': [],
    'qweb': [],
    'js':['static/src/js/invoice_print.js'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
