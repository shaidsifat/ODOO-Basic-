{
    'name': 'Hospital',
    'version': '1.0',
    'sequence': 2,
    'category': 'hospital',
    'summary':'Hospital Management System',
    'depends': ['base','contacts','sale'],
    'auto_install': False,
    'application': True,
    'installable': True,
    'data':[

        "views/res_partner_form_view.xml",
        "views/hospital_view.xml",
        "views/patient_view.xml",
        "views/appointment_view.xml",
        "views/doctor_view.xml",
        "views/employee.xml",



        "wizards/appointment_wzd_view.xml",
        "wizards/create_appointment.xml",

        "data/data.xml",

        "reports/appointment_pdf.xml",
        "reports/appointment_report_details_view.xml",
        "reports/barcode_template.xml",
        "reports/doctor_profile_barcode.xml",
        "reports/patient.xml",
        "reports/report.xml",
        "reports/report_action_details.xml",
        "reports/wizard_report.xml"
    ]
}


