# -*- coding: utf-8 -*-
{
    'name': 'Location Wise Transfer Report',
    'version': '1.0',
    'summary': 'Inventory Product location wise transfer report ',
    'sequence': 3,
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
        'reports/pdf_action_window.xml',
        'reports/product_sale_report_view.xml',
        'wizards/product_sale_wzd_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
