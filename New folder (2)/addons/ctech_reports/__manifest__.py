# -*- coding: utf-8 -*-
{
    'name': 'Ctech Reports',
    'version': '1.0',
    'summary': 'Inventory and billing billing rebuilt custom report collection',
    'sequence': 2,
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
        'reports/pdf_action_product_sale.xml',
        'reports/single_bill_collection_report_view.xml',
        'reports/multiple_bill_collection_report_view.xml',
        'reports/test_bill_collection_report_view.xml',
        'reports/all_department_collection_report_view.xml',
        'reports/single_dept_bill_collection_report_view.xml',

        'wizards/single_bill_collection_wzd_view.xml',
        'wizards/multiple_bill_collection_wzd_view.xml',
        'wizards/test_bill_collection_wzd_view.xml',
        'wizards/all_department_bill_collection_view.xml',
        'wizards/single_department_bill_collection_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
