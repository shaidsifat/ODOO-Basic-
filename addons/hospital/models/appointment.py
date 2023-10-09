from odoo import api, models, fields, _


class Appointment(models.Model):
    _name = "appointment.profile"

    patient_id = fields.Many2one('patient.userprofile', string="Patient Name")
    patient_phone = fields.Char(string="Patient Phone")
    age = fields.Char(string="age")
    gender = fields.Selection([('M', 'Male'),
                               ('F', 'Female')],
                              string="Gender",
                              help="Please select hospital type.",
                              )
    appointment_dr_id = fields.Many2one('doctor.profile', string=" Appointment Doctor")
    date = fields.Date(string="Date")

    @api.onchange('patient_id')
    def _onchange_patient_age_gender_phone(self):
        self.age = self.patient_id.age
        self.patient_phone = self.patient_id.phone
        self.gender = self.patient_id.gender



