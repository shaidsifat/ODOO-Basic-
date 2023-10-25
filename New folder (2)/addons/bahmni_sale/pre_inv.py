from odoo import fields, models, api, _

class PreInv(models.TransientModel):
    _name = 'pre.inv'

    id_order = fields.Many2one('sale.order', string='Order Reference', ondelete='cascade', index=True,
                               copy=False)

    id_product = fields.Many2one('product.product', string='Product', domain=[('sale_ok', '=', True)],
                                 change_default=True, ondelete='restrict',)
    uom_qty_product = fields.Float(string='Quantity',
                                   default=1.0)
    unit_price= fields.Float('Unit Price', default=0.0)

    price_subtotal = fields.Float( string='Subtotal', readonly=True, store=True)






