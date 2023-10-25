from odoo import models, api, fields

'''
    product_delivery_report" is folder name and "product_shop_wise_delivery" is template name
'''


class WizardProductDeliver(models.TransientModel):
    _name = 'expire.product.report'

    start_date = fields.Datetime(string='From Date')
    end_date = fields.Datetime(string='End Date')
    locat_id = fields.Many2one('stock.location', string='Location')

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'expire_product_report.date_wise_expire_report', data=data)
