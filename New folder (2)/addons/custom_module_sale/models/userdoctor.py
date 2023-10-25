from odoo import api, models, fields, _
from odoo.exceptions import ValidationError


class InheritDoctorProfile(models.Model):

    _inherit = "doctor.profile"



    doctor_ref = fields.Char(string='Doctor Reffernce', required=True, copy=False, readonly=False,
                           default=lambda self: _('/'))

    @api.model
    def create(self, vals):

        if vals.get('doctor_ref',False) != "/":
            doctor_ref_id = self.env['doctor.profile'].search([('doctor_ref', '=',vals.get('doctor_ref'))])
            if  doctor_ref_id:
                raise ValidationError(
                    "This reference is already exists! kindly put another unique reference of a doctor")
            else:
                return super(InheritDoctorProfile, self).create(vals)

        if vals.get('doctor_ref', _('/')) == _('/'):
            vals['doctor_ref'] = self.env['ir.sequence'].next_by_code('doctor.profile') or _('/')

        return super(InheritDoctorProfile, self).create(vals)



    @api.multi
    def write(self,values):

        if values.get('doctor_ref', False):
            doctor_ref_id = self.env['doctor.profile'].search([('doctor_ref', '=', values.get('doctor_ref'))])

            if doctor_ref_id:
                raise ValidationError(_("The Value is found.The Doctor referrence id is  alreday exist FOr write."))

        res = super(InheritDoctorProfile, self).write(values)
        return res
