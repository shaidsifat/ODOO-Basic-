from odoo import api, fields, models, _


class Product(models.Model):

    _name = "product.sale"


    sale_order_ids = fields.Many2one('sale.product', string="sale_order", readonly=True)
    product_name =  fields.Char(string="Product Name")
    product_price = fields.Integer(string="product_price")


class SaleOrder(models.Model):

    _name = "sale.product"

    patient = fields.Many2one('patient.userprofile', string="Patient Name")
    # product_ids = fields.One2many('product.product.template', 'sale_order_id', string="Product list")
    amount = fields.Integer(string="Refund Amount", required=True)
    is_refund = fields.Boolean(string="Is Refund", default=True)
    product_ids = fields.One2many('product.sale', 'sale_order_ids', string="Product list")
    qunatity = fields.Integer(string="Product Quantity")


