from odoo import fields, models, api

class RegistrationOrder(models.Model):
    _name = "registration.order"
    _description = "Registration Order"

    partner_ref = fields.Char(string = "Internal Referenc")
    partner_uuid = fields.Char(string = "UUID")
    so_create_date = fields.Date(string ="SO create date")
    discount_type = fields.Selection([('free','Free'),('paid','Paid')],string = "Discount Type")
    price = fields.Float(string = "Ticket Price")
    is_so_created = fields.Boolean(string="Is So Created?",default = False)