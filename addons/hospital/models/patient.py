from odoo import api, models, fields, _
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import ValidationError
class PatientUserProfile(models.Model):

    _name = "patient.userprofile"

    name = fields.Char(string="Patient Name")
    phone = fields.Char(string="Phones")
    age = fields.Char(string="Age" , compute="_compute_age")
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')],
                              string="Gender",
                              help="Please select hospital type.",)
    dob = fields.Date(string="DOB")
    address = fields.Text()
    appointments_ids = fields.One2many('appointment.profile','patient_id')
    patient_ref = fields.Char(string="Patient Reference Number", required=True, copy=False, readonly=False,default=lambda self: _('New'))
    @api.depends("dob")
    def _compute_age(self):
       for record in self:
           if record.dob:
               year =  relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).years
               month = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).months
               day = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).days
               age = str(year) + " " + " Y " + str(month) + " " + " M " + str(day) + " " + " D "
               record.age = age
           else:
               record.age = 0
    @api.model
    def create(self,vals):
            # if vals.get('patient_ref', _('New')) == _('New'):
            #
            #     patient_ref_id = self.env['patient.userprofile'].search([('patient_ref', '=', self.patient_ref)])
            #     print patient_ref_id
            #     if patient_ref_id == 0:
            #         raise ValidationError(
            #             _("The Value is found.The patient referrence id is  alreday exist FOr create."))
            #     else:
            #         if 'company_id' in vals:
            #             print 'company_id'
            #             vals['patient_ref'] = self.env['ir.sequence'].next_by_code('patient.userprofile') or _('New')
            #         else:
            #             vals['patient_ref'] = self.env['ir.sequence'].next_by_code('patient.userprofile') or _('New')
            if vals.get('patient_ref') != "New":
                patient_ref_id = self.env['patient.userprofile'].search([('patient_ref', '=', vals.get('patient_ref'))])
                if patient_ref_id:
                    raise ValidationError("This reference is already exists! kindly put another unique reference of a patient")

            if vals.get('patient_ref', _('New')) == _('New'):
                vals['patient_ref'] = self.env['ir.sequence'].next_by_code('patient.userprofile') or _('New')

            result = super(PatientUserProfile, self).create(vals)
            return result
    @api.onchange('patient_ref')
    def _onchange_patient_ref_service(self):
            patient_ref_id = self.env['patient.userprofile'].search([('patient_ref','=',self.patient_ref)])
           # print   patient_ref_id
            if  patient_ref_id:
                raise ValidationError(_("The Value is found.The patient referrence id is  alreday exist."))
    @api.multi
    def write(self,values):
        patient_ref_id =  self.env['patient.userprofile'].search([('patient_ref', '=', values.get('patient_ref'))])
        if patient_ref_id:
            raise ValidationError(_("The Value is found.The patient referrence id is  alreday exist FOr write."))
        res = super(PatientUserProfile, self).write(values)
        return res




