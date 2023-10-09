# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

# from odoo import api, models, fields
from odoo import api, models, fields, _
class Patient(models.Model):

     _name = "patient.profile"

     name = fields.Char(string="Patient Name")
     email = fields.Char()
     phone = fields.Char(string="Phones")
     age = fields.Integer(string="Age")
     gender = fields.Selection([('male', 'Male'),
                                ('female', 'Female')],
                                string="Gender",
                                help="Please select hospital type.",
                                default='female'
                               )
     demo = fields.Char()
     Dob = fields.Date()
     name_seq = fields.Char(string='order Reference',required=True,copy=False,readonly=True, default=lambda self: _('New'))
     @api.model
     def create(self,vals):
         if vals.get('name_seq', _('New')) == _('New'):
             if 'company_id' in vals:
                vals['name_seq'] = self.env['ir.sequence'].with_context(force_company=vals['çompany_id']).next_by_code('sale.order') or _('New')
             else:
                 vals['name_seq'] = self.env['ir.sequence'].next_by_code('sale.order') or _('New')
         result = super(Patient,self).create(vals)
         return result




