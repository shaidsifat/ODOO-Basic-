from odoo import models, api, fields

'''
    product_delivery_report" is folder name and "product_shop_wise_delivery" is template name
'''

class WizardProductDeliver(models.TransientModel):
    _name = 'wizard.product.category.modified'

    start_date = fields.Datetime(string='From Date')
    end_date = fields.Datetime(string='End Date')
    ctg_id = fields.Many2one('product.category', string='Category Name')

    @api.multi
    def print_report(self, data):
        return self.env['report'].get_action(self, 'category_report_modified.category_wise_delivery_modified', data=data)
