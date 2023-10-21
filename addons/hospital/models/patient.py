import json

from odoo import api, models, fields, _
from odoo import models, fields, api, exceptions
from dateutil.relativedelta import relativedelta
from datetime import datetime
from odoo.exceptions import ValidationError
class PatientUserProfile(models.Model):

    _name = "patient.userprofile"
    _rec_name = "patient_id"

    # name = fields.Char(string="Name")
    # name = fields. Char(default="Extended")
    # name = fields.Char('res.partner','supplier.name')
    patient_id = fields.Many2one('res.partner',string='Patient Name',)
    phone = fields.Char(string="Phones")
    age = fields.Char(string="Age",compute="_compute_age")
    gender = fields.Selection([('male', 'Male'),
                               ('female', 'Female')],

                              string="Gender",
                              help="Please select hospital type.",)
    dob = fields.Date(string="DOB")
    address = fields.Text()
    appointments_ids = fields.One2many('appointment.profile','patient_id')
    # patient_ref = fields.Char(string="Patient Reference Number", required=True, copy=False, readonly=False,default=lambda self: _('New'))
    patient_ref = fields.Char(string="Patient Reference Number")
    is_patient = fields.Boolean(string="Is Patient", default=False)

    @api.depends("dob")
    def _compute_age(self):
        for record in self:
            if record.dob:
                year = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).years
                month = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).months
                day = relativedelta(datetime.now().date(), datetime.strptime(record.dob, '%Y-%m-%d')).days
                age = str(year) + " " + " Y " + str(month) + " " + " M " + str(day) + " " + " D "
                record.age = age
            else:
                record.age = 0

    @api.model
    def create(self, vals):


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

        # if vals.get('patient_ref') != "New":
        #     patient_ref_id = self.env['patient.userprofile'].search([('patient_ref', '=', vals.get('patient_ref'))])
        #     if patient_ref_id:
        #         raise ValidationError(
        #             "This reference is already exists! kindly put another unique reference of a patient")
        #
        # if vals.get('patient_ref', _('New')) == _('New'):
        #     vals['patient_ref'] = self.env['ir.sequence'].next_by_code('patient.userprofile') or _('New')
        print vals
        print vals['patient_id']
        print ".....patient_id.......",self.patient_id
        data1 = self.env['res.partner'].search( [ ('id','=',vals['patient_id']  ) ] )

        print data1
        print "..... phone .......",self.appointments_ids

        # patient_data =  dict(self.fields['gender'].selection).get(self.gender)
        print "............patient_data.........."

        # Set the computed field value to the gender label

        # print "sifat", dict(vals.fields['gender'].selection).get(vals.gender)

        @api.multi
        def my_function(self):
           print("...... new my_function.....")
           print type(self.gender)
           if self.id:

               data = self.env['patient.userprofile'].browse(self.id)

               # nice = (data._fields['gender'].selection).get(data.gender,False)
               gender =  dict(data._fields['gender'].selection).get(data.gender)
               non=data1.write({'gender': gender})
               print non
               return  non
               # for new_data in data:
               #
               #     data['gender'] = dict(new_data._fields['gender'].selection).get(new_data.gender,False)
               #     print(data['gender'])

               print("None")
           print("Not")

        for x in data1:

            if  x.id:
                #res= self.env['patient.userprofile'].browse(x.id)

                gender= vals['gender']
                dob = vals['dob']
                date_of_birth = vals['dob']
                phone = vals['phone']
                street = vals['address']
                # age = vals['age']
                print str(gender)
                data1.write({'date_of_birth': str(dob),'mobile': str(phone),'street': str(street)})

        # data = self.env['res.partner'].search( [  ('id','=',vals['patient_id']  ) ] )#create({'age':self.age,'gender':self.gender})
        result = super(PatientUserProfile, self).create(vals)
        return result

    @api.onchange('patient_ref')
    def _onchange_patient_ref_service(self):
        patient_ref_id = self.env['patient.userprofile'].search([('patient_ref', '=', self.patient_ref)])
        print  patient_ref_id
        if patient_ref_id:
            raise ValidationError(_("The Value is found.The patient referrence id is  alreday exist."))

    @api.multi
    def write(self, vals):
        # patient_ref_id = self.env['patient.userprofile'].search([('patient_ref', '=', values.get('patient_ref'))])
          #     raise ValidationError(_("The Value is found.The patient referrence id is  alreday exist FOr write."))
        # res = super(PatientUserProfile, self).write(values)
        # return res
        print vals
        if 'patient_id' in vals:
            data1 = self.env['res.partner'].search([('id', '=', vals['patient_id'])])

            print data1

            # gender = dict(appointment_id._fields['gender'].selection).get(
            #     appointment_id.gender,
            #     False)
            for x in data1:
                if x.id :
                    # res= self.env['patient.userprofile'].browse(x.id)
                    dob = vals['dob']
                    date_of_birth = vals['dob']
                    phone = vals['phone']
                    street = vals['address']
                    gender = dict(vals._fields['gender'].selection).get(vals.gender,False)
                    print gender
                    # age = vals['age']
                    # print str(gender)
                    print dob
                    data1.write({'date_of_birth': str(dob), 'mobile': str(phone), 'street': str(street),})
        # data = self.env['res.partner'].search( [  ('id','=',vals['patient_id']  ) ] )#create({'age':self.age,'gender':self.gender})
        else:
            raise exceptions.Warning("please give proper all  data")
        result = super(PatientUserProfile, self).create(vals)
        return result
