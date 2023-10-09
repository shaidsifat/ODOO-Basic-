from odoo import models, api, fields
from datetime import datetime, timedelta


class WizardProductSale(models.TransientModel):
    _name = 'custom.single.department.collection'

    start_date = fields.Datetime(string='From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now(), required=True)
    user_ids = fields.Many2many('res.users', string="Billing User")
    categ_id = fields.Many2one('product.category', 'Product category', required=False)

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'ctech_reports.single_department_bill', data=data)

