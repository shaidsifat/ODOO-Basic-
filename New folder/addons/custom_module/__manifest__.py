{
    'name': 'Custom Module',
    'version': '1.0',
    'sequence': '1',
    'category': 'Custom',
    'summary':'Custom Hospital Management System',
    'depends': ['base','hospital','sale'],
    'data':[
        'views/inherit_doctor_form_view.xml',
        'data/data.xml'
    ]
    ,
    'auto_install': False,
    'application': True,
    'installable': True,
}




