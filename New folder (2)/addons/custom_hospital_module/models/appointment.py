from odoo import api, models, fields, _

class HospitalAppointment(models.Model):

    _name = "appointment.hospital"

    patient_ids = fields.Many2one('hospital.patient','name')
    patientphone = fields.Char(string="Patient Phone")
    age = fields.Char(string="age")
    gender =  fields.Selection([('male', 'Male'),
                                ('female', 'Female')],
                                string="Gender",
                                help="Please select hospital type.",
                               )
    appointment_dr = fields.Many2one('doctor.profile','name')
    date = fields.Date(string="Date")


