from odoo import models, api, fields
from datetime import datetime, timedelta

'''
    ctech_reports" is folder name and "test_bill_report" is report template id
'''


class WizardProductSale(models.TransientModel):
    _name = 'custom.test.collection'

    start_date = fields.Datetime(string='From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now(), required=True)
    user_id = fields.Many2one('res.users', string='Billing User')

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'ctech_reports.test_bill_report', data=data)

