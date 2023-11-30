from odoo import models, api, fields
from datetime import datetime, timedelta

'''
    ctech_reports" is folder name and "test_wise_single_department_report" is report template id
'''


class WizardProductSale(models.TransientModel):
    _name = 'custom.test.single.dept'

    start_date = fields.Datetime(string='From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now(), required=True)
    user_ids = fields.Many2many('res.users', string='Billing User')
    categ_id = fields.Many2one('product.category', 'Product category', required=False)

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'ctech_reports.test_single_dept_report', data=data)
