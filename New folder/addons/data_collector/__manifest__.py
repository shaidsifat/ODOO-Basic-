{
    'name': 'Data Collector',
    'summary': """This module Developed for collect Data""",
    'version': '1.0.0',
    'description': """This is for collecting category wise data  """,
    'author': 'Crystal Technology Bangladesh Ltd.',
    'company': 'cTechbd',
    'website': 'https://www.ctechbd.com',
    'category': 'Tools',
    'depends': ['base', 'sale','account'],
    'license': 'AGPL-3',
    'sequence': 1,
    'data':[
        'views/view.xml',
        'views/menu.xml'
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}
