from odoo import api, models, fields



class ResPartner(models.Model):
    _inherit = 'res.partner'

    is_patient = fields.Boolean(string="Is Patient")

    @api.model
    def create(self, vals):
        print vals
        print "first age",vals
        if self._context.get('model',False) == 'patient.profile':
            vals["is_patient"] = True
            vals['date_of_birth'] = self.age

        res = super(ResPartner, self).create(vals)
        return res