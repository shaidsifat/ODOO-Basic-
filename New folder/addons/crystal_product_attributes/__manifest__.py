# -*- coding: utf-8 -*-
{
    'name': 'Crystal Product Attributes',
    'version': '1.0',
    'summary': 'Custom Crystal Product Attributes module to meet requirement',
    'sequence': 1,
    'description': """
Crystal Product Attributes
====================
""",
    'category': 'Stock',
    'website': '',
    'images': [],
    'depends': ['base', 'sale', 'stock', 'bahmni_sale', 'product'],
    'data': [
        'security/ir.model.access.csv',
        'views/product_attributes_tree_view.xml',
        'views/product_template.xml',
        'views/sale_order_view.xml',
    ],
    'demo': [],
    'qweb': [],
    'installable': True,
    'application': True,
    'auto_install': False,
}
