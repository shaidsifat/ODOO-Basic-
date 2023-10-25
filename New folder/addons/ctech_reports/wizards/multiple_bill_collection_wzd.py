from odoo import models, api, fields
from datetime import datetime, timedelta

class WizardProductSale(models.TransientModel):
    _name = 'custom.multiple.bill.collection'

    start_date = fields.Datetime(string='From Date', default=fields.Datetime.now(), required=True)
    end_date = fields.Datetime(string='End Date', default=fields.Datetime.now(), required=True)

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'ctech_reports.multiple_user_bill_collection_report', data=data)

