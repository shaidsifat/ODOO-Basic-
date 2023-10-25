from odoo import fields, models, api, _

class DepartmentWiseCollection(models.Model):
    _name = 'department.wise.collection'

    name=fields.Char('Department')
    total_amount=fields.Float('Total Amount')
    categ_id=fields.Integer('Category ID')

