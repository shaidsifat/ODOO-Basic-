from odoo import fields, models, api, _

class LabOrder(models.Model):
    _name = "lab.order"
    _description = "Lab Order"

    partner_id = fields.Many2one('res.partner',string="Patient")
    partner_identifier = fields.Char(string="Patient Identifier")
    sale_id = fields.Many2one('sale.order',string="Sale Order")
    invoice_id = fields.Many2one('account.invoice',string="Invoice Id")
    age =  fields.Char(string = "Age",default = False)
    gender = fields.Selection([('M','Male'),('F','Female'),('O','Others')] ,string = "Gender")
    net_amount = fields.Float(string="Net Amount")
    is_free = fields.Boolean(string="Is Free?")
    is_refund = fields.Boolean(string="Is Refund?")
    lab_order_line_ids = fields.One2many('lab.order.line','lab_order_id',string="Lab Order Lines")

class LabOrderLine(models.Model):
    _name = "lab.order.line"
    _description = "lab Order Line"

    product_id = fields.Many2one('product.product',string="Product")
    name = fields.Char(string = "Product Name")
    quantity = fields.Float(string="Quantity")
    price_unit = fields.Float(string="Price Unit")
    lab_order_id = fields.Many2one('lab.order',string = "Lab Order Id")
    uuid = fields.Char(string="UUID")
