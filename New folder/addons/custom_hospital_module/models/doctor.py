
from odoo import api, models, fields, _
from odoo.exceptions import ValidationError

class HospitalDegree(models.Model):

    _name = "hospitaldoctor.degree"
    _rec_name = "name"
    #doctor = fields.One2many('doctor.profile',string="doctor.profile")
    name = fields.Char(string="Degree_Name")
    doctor_id = fields.Many2one('hospitaldoctor.profile', string="Doctor")

class HospitalDoctor(models.Model):

    _name ="hospitaldoctor.profile"
    _rec_name = "name"

    name = fields.Char(string="Doctor Name")
    age = fields.Char(string="DoctorAge")
    gender = fields.Selection([('male','Male'),
                               ('female','Female')],)
    dob = fields.Date()
    institution = fields.Char()
    #degree_ids = fields.Many2many('doctor.degree', string="Degrees")
    degree_ids = fields.One2many('hospitaldoctor.degree','doctor_id',string="Degrees")
    #degree_ids = fields.Many2one('doctor.degree','name')
    appointment_ids = fields.One2many('appointment.profile','appointment_dr',string="appointment_ids")

class Doctor(models.Model):

    _name = "Doctor.profile"

    doc_ref = fields.Char(string="Doctor  Reference Number", required=True, copy=False, readonly=False,
                              default=lambda self: _('New'))

    @api.model
    def create(self, vals):


        if vals.get('doc_ref') != "New":

            patient_ref_id = self.env['Doctor.profile'].search([('doc_ref', '=', vals.get('doc_ref'))])
            if patient_ref_id:
                raise ValidationError(
                    "This reference is already exists! kindly put another unique reference of a doctor")

            if vals.get('doc_ref', _('New')) == _('New'):
                vals['doc_ref'] = self.env['ir.sequence'].next_by_code('Doctor.profile') or _('New')

            result = super(Doctor, self).create(vals)
            return result

