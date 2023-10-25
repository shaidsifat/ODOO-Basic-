
from odoo import api,fields,models
from odoo import models, fields, api
from datetime import datetime, timedelta

# AppointmentReportWizard model
class AppointmentReportWizard(models.TransientModel):

        _name='report.wizard'
        _description="Print Appointment Wizard"

        patient_id = fields.Many2one('patient.userprofile',string="Patient")
        date_form = fields.Date(string="Date From")
        date_to = fields.Date(string="Date to")
        # @api.multi
        # def action_print_report(self):
        #
        #       appointments = self.env['appointment.profile'].search_read([])
        #       # data = {
        #       #    'form_data': self.read()[0],
        #       # }
        #       # return self.env['report'].get_action(self,'appointment.profile',data=data)
        #
        #       vals = {
        #           'form_data': self.read()[0],
        #       }
        #       return self.env['appointment.profile'].get_action(self, 'appointment.profile', data=vals)
        #       # appointment_id =  self.env.ref['appointment.profile'].get_action((self,'appointment.profile',data=vals)

        @api.multi
        def action_print_report(self, data):

            # Issued/ transfer balance calculation
            # query = self.env['appointment.profile'].search_read([])
            # # passing the data for render
            # data = {
            #     'list': query,
            # }


            # return self.env['ir.actions.report'].get_action(self, 'appointment.profile', data=data)
            # return self.env['action_report_appointment'].sudo().get_action([self.id])
            return self.env['report'].get_action(self, 'hospital.appointment_template_id', data=data)





