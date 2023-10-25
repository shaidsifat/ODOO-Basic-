
from odoo import api, fields, models, _


class RefundProduct(models.Model):
    _name = "refund.product"

    product_ids  = fields.One2many('product.sale', 'sale_order_ids', string="Product list")
    amount       =   fields.Integer(string="Refund Amount",required= True)




