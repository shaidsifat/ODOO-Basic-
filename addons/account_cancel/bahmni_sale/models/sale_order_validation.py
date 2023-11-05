from odoo import models, api, fields
from odoo.exceptions import ValidationError


class SaleOrderValidation(models.Model):
    _inherit = "sale.order"

    @api.multi
    # @api.constrains('order_line')-u can't apply constrains in overrriden method in odoo
    def action_confirm(self):
        res = super(SaleOrderValidation, self).action_confirm()
        self.validate_order_line()

        return res

    @api.constrains('order_line')
    # constrain should be managed here since this is the function for
    def validate_order_line(self):
        for added_product in self:
            exist_product_list = []
            for line in added_product.order_line:
                if line.product_id.id in exist_product_list:
                    raise ValidationError(('You can not add same service more than once !!!!!'))
                exist_product_list.append(line.product_id.id)
