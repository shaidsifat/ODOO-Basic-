{
    'name': 'Hospital Module',
    'version': '1.0',
    'sequence': '3',
    'category': 'hospital',
    'summary':'Custom Hospital Management System',
    'depends': ['base'],
    'data':[

        "views/patient_view.xml",
        "views/appointment.xml",

    ]
    ,
    'auto_install': False,
    'application': True,
    'installable': True,
}




