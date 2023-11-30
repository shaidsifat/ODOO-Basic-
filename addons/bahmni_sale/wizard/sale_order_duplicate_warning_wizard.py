from odoo import models, fields, api, _


class SaleOrderDuplicateWarningWizard(models.TransientModel):
    _name = "sale.order.duplicate.warning.wizard"
    
    
    def action_confirm(self):
        sale_order_id = self.env.context.get("sale_order_id")
        sale_order = self.env["sale.order"].browse(sale_order_id)
        sale_order.action_confirm()