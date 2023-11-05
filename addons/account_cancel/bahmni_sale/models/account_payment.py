from odoo import fields, models, api, _

class AccountPayment(models.Model):
    _inherit = "account.payment"


    @api.multi
    def post(self):
        """
        This function is extended for create lab category data in lab.order model
        """
        res = super(AccountPayment, self).post()
        invoice_id = self.invoice_ids.filtered(lambda inv : inv.type == 'out_invoice')
        if invoice_id:
            sale_origin =  invoice_id.origin
            sale_id = self.env['sale.order'].search([('name','=',sale_origin)])
            sale_id.with_context(invoice_sale_id = sale_id).action_create_lab_order()
            return res

        refund_invoice_id = self.invoice_ids.filtered(lambda inv : inv.type == 'out_refund').refund_invoice_id
        if refund_invoice_id:
            refund_invoice_id.has_refund = True
            sale_origin = refund_invoice_id.origin
            sale_id = self.env['sale.order'].search([('name','=',sale_origin)])
            sale_id.with_context(refund_invoice_sale_id = sale_id).action_create_lab_order()
            return res

        return res