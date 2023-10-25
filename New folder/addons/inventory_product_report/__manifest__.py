# -*- coding: utf-8 -*-
{
    'name': 'Inventory Product Report',
    'version': '1.0',
    'summary': 'Inventory Product Report module to meet supervisor requirement',
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
        'reports/pdf_action_inventory_product.xml',
        'reports/location_wise_product_report_view.xml',


        'reports/inherit_indent_stock_templete.xml',
        'reports/inherit_purchase_order_default_report.xml',
        'reports/inherit_purchase_quotation_default_report.xml',



        'wizards/location_wise_product_wzd_view.xml'
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
