# -*- coding: utf-8 -*-
{
    'name': 'Bahmni Sale',
    'version': '1.0',
    'summary': 'Custom Sales module to meet bahmni requirement',
    'sequence': 1,
    'description': """
Bahmni Sale
====================
""",
    'category': 'Sales',
    'website': '',
    'images': [],
    'depends': ['base','sale', 'sale_stock','sales_team', 'bahmni_account','point_of_sale','account','web','report','account'],
    'data': ['security/ir.model.access.csv',
             'security/security_groups.xml',
             'data/data.xml',
             'data/sale_config_setting.xml',
             'data/get_registration_data_cron_job.xml',
             'views/bahmni_sale.xml',
             'views/res_partner_view.xml',
             'views/village_master_view.xml',
             'views/sale_order_views.xml',
             'views/sale_config_settings.xml',
	         'views/pos_view.xml',
             'views/account_invoice_view.xml',
             'views/report_sale_invoice_view.xml',
             'views/report_refund_invoice_view.xml',

             ],
    'demo': [],
    'qweb': [],
    'js':['static/src/js/invoice_print.js'],
    'installable': True,
    'application': True,
    'auto_install': False,
}
