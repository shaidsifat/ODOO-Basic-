# -*- coding: utf-8 -*-
{
    'name': 'Scrap Product Report',
    'version': '1.0',
    'summary': 'Inventory Scrap Product Report module to meet supervisor requirement',
    'sequence': 4,
    'description': """
    Product Report
====================
""",
    'category': 'Report',
    'website': [],
    'images': [],
    'depends': ['base',
                'stock',
                'sale',
                'bahmni_sale',
                'purchase'
                ],
    'data': [
        'reports/pdf_action.xml',
        'reports/scrap_product_report_view.xml',
        'wizards/scrap_product_wizerd_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
