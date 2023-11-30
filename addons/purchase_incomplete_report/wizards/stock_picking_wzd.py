
from odoo import api,fields,models
from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportWizard(models.TransientModel):

        _name='report.stock_picking.wizard'
        _description="Print incomplete purchase order Wizard"

        start_date = fields.Datetime(string='From Date', default=fields.Datetime.now(), required=True)
        end_date = fields.Datetime(string='End Date', default=fields.Datetime.now(), required=True)

        @api.multi
        def action_print_report(self, data):

            return self.env['report'].get_action(self,'purchase_incomplete_report.purchase_template_id',data=data)





