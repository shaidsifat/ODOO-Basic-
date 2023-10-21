from odoo import api, models, fields, _
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Degree(models.Model):

    _name = "doctor.degree"
    _rec_name = "name"

    name = fields.Char(string="Degree_Name")
    doctor_id = fields.Many2one('Doctor.profile', string="Doctor")
    duration = fields.Integer(string="Degree_Duration")

class Doctor(models.Model):

    _name ="doctor.profile"
    _rec_name = "name"


    name = fields.Char(string="Doctor Name")
    age = fields.Char(string="DoctorAge",compute="_compute_person_age")
    gender = fields.Selection([('male','Male'),
                               ('female','Female')],)
    dob = fields.Date()
    institution = fields.Char()
    degree_ids = fields.One2many('doctor.degree', 'doctor_id', string="Degrees")
    # appointment_ids = fields.One2many('appointment.profile','appointment_dr_id',string="appointment_ids")
    @api.depends('dob')
    def _compute_person_age(self):
        for record in self:

            if record.dob:

                year = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).years
                month = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).months
                day = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).days
                age = str(year) + " " + " Y " + str(month) + " " + " M " + str(day) + " " + " D "
                record.age = age
            else:
                record.age = 0
    # @api.depends("dob")
    # def _compute_age(self):
    #
    #    for record in self:
    #        if record.dob:
    #            year =  relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).years
    #            month = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).months
    #            day = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).days
    #            age = str(year) + " " + " Y " + str(month) + " " + " M " + str(day) + " " + " D "
    #            record.age = age
    #        else:
    #            record.age = 0