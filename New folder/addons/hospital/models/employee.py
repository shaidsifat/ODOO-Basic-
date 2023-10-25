from odoo import api, models, fields, _
from dateutil.relativedelta import relativedelta
from datetime import datetime


class Employee(models.Model):

    _name = "emp.profile"

    name = fields.Char(string="Employee_Name")
    designation = fields.Selection([('staff','Staff'),
                               ('doctor','Doctor'),
                              ('intern_doctor','Intern_Doctor')],)
    dob = fields.Date(string="Date of Birth")



