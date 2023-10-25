
from odoo import fields, models, api, _

class PreviousInvoice(models.TransientModel):
    _name='previous.invoice'

    # @api.multi
    # @api.depends('partner_id')
    # def _in_count(self):
    #     self.patient_id = self.env['account.invoice'].search_count([()])
    #     print self.patient_id
    #     print "Function Call"
    #     return self.patient_id
    @api.multi
    def _default_partner(self):
        self.partner_id= self.env['sale.order'].browse(self._context.get('partner_id'))
        return self.partner_id

    @api.multi
    def _get_date(self):
        self.inv_date = self.env['sale.order'].browse(self._context.get('inv_date'))
        return self.inv_date

    partner_id=fields.Many2one('res.partner',string='Patient',track_visibility='always',compute=_default_partner, readonly=False)
    inv_date=fields.Date(string='Order Date',compute=_get_date,readonly=False)







