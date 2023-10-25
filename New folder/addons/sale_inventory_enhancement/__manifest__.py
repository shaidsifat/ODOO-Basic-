# -*- coding: utf-8 -*-
{
    'name': 'Sale Inventory Enhancement',
    'version': '1.0',
    'summary': 'Sale Inventory Enhancement',
    'sequence': 4,
    'description': """
    Product Report
====================
""",
    'category': 'Report',
    'website': '',
    'images': [],
    'depends': ['base','stock','sale','bahmni_sale', 'purchase'],
    'data': [
             'reports/pdf_action.xml',
             ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
