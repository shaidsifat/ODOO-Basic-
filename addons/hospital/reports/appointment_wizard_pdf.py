from odoo import models, fields, api
from datetime import datetime, timedelta


class ReportAppointment(models.AbstractModel):

    _name = 'report.hospital.appointment_template_id'

    def data_for_report(self, start_date, end_date, patient_id):

        data_list = []
        if not patient_id:
            domain = [
                ('date', '>=', start_date), ('date', '<=', end_date)
            ]
            appointment_ids = self.env['appointment.profile'].search(domain)

            print appointment_ids

            for appointment_id in appointment_ids:

                appointment_data = {}
                appointment_data['patient_id'] = appointment_id.patient_id.name
                appointment_data['patient_phone'] = appointment_id.patient_phone
                appointment_data['age'] = appointment_id.age
                appointment_data['gender'] = dict(appointment_id._fields['gender'].selection).get(appointment_id.gender,
                                                                                                  False)
                appointment_data['appointment_dr_id'] = appointment_id.appointment_dr_id
                appointment_data['date'] = appointment_id.date
                data_list.append(appointment_data)

        else:
            domain = [
                ('date', '>=', start_date), ('date', '<=', end_date), ('patient_id', '=', patient_id.id)
            ]
            appointment_ids = self.env['appointment.profile'].search(domain)

            for appointment_id in appointment_ids:
                appointment_data = {}
                appointment_data['patient_id'] = appointment_id.patient_id.name
                appointment_data['patient_phone'] = appointment_id.patient_phone
                appointment_data['age'] = appointment_id.age
                appointment_data['gender'] = dict(appointment_id._fields['gender'].selection).get(appointment_id.gender,
                                                                                                  False)
                appointment_data['appointment_dr_id'] = appointment_id.appointment_dr_id
                appointment_data['date'] = appointment_id.date
                data_list.append(appointment_data)

        return data_list


    @api.model
    def render_html(self, docsid, data=None):
        self.model = self.env.context.get('active_model')
        docs = self.env[self.model].browse(self.env.context.get('active_id'))
        report_obj = self.env['report']
        report = report_obj._get_report_from_name('hospital.appointment_template_id')
        final_data = self.data_for_report(docs.date_form, docs.date_to, docs.patient_id)

        docargs = {

            'final_data': final_data
        }

        print "final_data",docargs['final_data']

        return self.env['report'].render('hospital.appointment_template_id',docargs)
