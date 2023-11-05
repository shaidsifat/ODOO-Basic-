from odoo import fields, models, api, _
from odoo.exceptions import ValidationError

class AccountPayment(models.Model):
    _inherit = "account.payment"

    @api.multi
    def post(self):
        res = super(AccountPayment, self).post()
        refund_invoice_id = self.invoice_ids.filtered(lambda inv: inv.type == 'out_refund').refund_invoice_id
        if refund_invoice_id:
            sale_order_id = self.env["sale.order"].search([('name','=',refund_invoice_id.origin)])
            sale_order_id.is_sale_order_refund = True
        return res
