from odoo import models,fields
from datetime import datetime

class ReportModel(models.Model):
    _name = 'report.model'

    opening_balance = fields.Integer('Opening Balance')
    receipt_balance = fields.Integer('Receipt Balance')
    present_balance = fields.Integer('Present Balance')
    issued_balance = fields.Integer('Issued Balance')
    closing_balance = fields.Integer('Closing Balance')
    product_id = fields.Many2one('product.product')
    previous_date = fields.Datetime(string='previous Date')
    after_date = fields.Datetime(string='After Date')



