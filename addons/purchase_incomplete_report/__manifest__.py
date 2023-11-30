{
    'name': 'Purchase Incomplete report',
    'version': '1.0',
    'sequence': 2,
    'category': 'purchase',
    'summary':'Purchase Incomplete report',
    'depends': ['base','contacts','sale'],
    'auto_install': False,
    'application': True,
    'installable': True,



    'data':[

        "wizards/stock_picking_wzd.xml",
        "reports/stock_picking.xml",
    ]
}


