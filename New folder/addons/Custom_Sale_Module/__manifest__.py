{
    'name':             'Sale_Custom_Module',
    'version':          '1.0',
    'sequence':         '1',
    'category':         'Custom',
    'summary':         'Custom Sale Module',
    'depends':         ['base','hospital','product'],
    'data':            [

                          'views/customer_view.xml',
                          'views/sale_product_view.xml',
                          'views/refund_view.xml',

                          'report/refund_report_view.xml',
                          'report/report_action_view.xml',


                        ],
    'auto_install':    True,
    'application':     True,
    'installable':     True,
}




