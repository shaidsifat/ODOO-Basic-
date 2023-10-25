from odoo import models,fields, api

class CreateAppointment(models.TransientModel):

    _name = 'create.appointment'

    date_appointment = fields.Date(string='Appointment Date', required=False)
    patient_id = fields.Many2one('patient.userprofile',string="Patient Id", required=True)
    doctor_id = fields.Many2one('doctor.profile',string="Appointment Doctor",required=True)

    def button_action_create_appointment(self):
           vals = {
                'patient_id': self.patient_id.id,
                'appointment_dr_id': self.doctor_id.id,
                'date': self.date_appointment
           }
           print vals
           appointment_id = self.env['appointment.profile'].create(vals)
           appointment_id._onchange_patient_age_gender_phone()

