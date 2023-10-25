# -*- coding: utf-8 -*-
{
    'name': 'Expire Product Report',
    'version': '1.0',
    'summary': 'Product Report module to meet supervisor requirement',
    'sequence': 4,
    'description': """
    Product Report
====================
""",
    'category': 'Report',
    'website': 'odoomates.com',
    'images': [],
    'depends': ['base','stock','sale','bahmni_sale', 'purchase'],
    'data': [
             'reports/pdf_action.xml',
             'reports/report_date_wise_expire_view.xml',
             'wizards/expire_products_report_view.xml',
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
