from odoo import models, fields, api


class ProductAttributes(models.Model):
    _name = "product.attributes"
    _rec_name = "name"

    name = fields.Char(string="Attributes Name")
    type = fields.Selection([('digital', 'Digital'), ('analogue', 'Analogue')], string='Type')
    product_id = fields.Many2one("product.template", string="Product")
    unit_price = fields.Float(string="Unit Price")


class Product(models.Model):
    _inherit = "product.template"

    attribute_ids = fields.One2many('product.attributes', 'product_id', string="Variants")


class SaleOrderLine(models.Model):
    _inherit = "sale.order.line"

    attributes_id = fields.Many2one("product.attributes", string="Attributes", store=True)
    is_required = fields.Boolean(string="Is Required", default=False)

    @api.onchange("attributes_id")
    def _onchange_attribute_id(self):
        for rec in self:
            if rec.product_id.product_tmpl_id.attribute_ids:
                rec.is_required = True
                rec.price_unit = rec.attributes_id.unit_price

    @api.onchange("product_id")
    def _onchange_domain_attributes_id(self):
        domain = list()
        for rec in self:
            domain.append(('id', 'in', rec.product_id.product_tmpl_id.attribute_ids.ids))
            if rec.product_id.product_tmpl_id.attribute_ids.ids:
                rec.is_required = True

        return {'domain': {'attributes_id': domain}}

