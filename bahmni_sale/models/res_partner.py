# -*- coding: utf-8 -*-
from odoo import models, fields, api
from dateutil.relativedelta import relativedelta
from datetime import datetime, date
from odoo.exceptions import UserError, ValidationError
import requests
import json
import logging

_logger = logging.getLogger(__name__)


class ResPartner(models.Model):
    _inherit = 'res.partner'

    # ref field is a default field of this class
    _sql_constraints = [('unique_ref', 'unique(ref)',
                         'Internal Reference for Customer should be unique!')]

    village_id = fields.Many2one('village.village', string="Village")
    tehsil_id = fields.Many2one('district.tehsil', string="Tehsil")
    district_id = fields.Many2one('state.district', string="District")
    local_name = fields.Char(string="Local Name")
    uuid = fields.Char(string="UUID")
    attribute_ids = fields.One2many('res.partner.attributes', 'partner_id', string='Attributes')
    age = fields.Char(string="Age", compute="_compute_age")
    gender = fields.Selection([('M', 'Male'), ('F', 'Female'), ('O', 'Others')], string="Gender")
    date_of_birth = fields.Date(string="Date of Birth")

    # inherited to update display name w.r.t. ref field
    # and hence user can search customer with reference too

    @api.multi
    def _get_age_gender(self, uuid):
        """
        Function is implemented for get age and gender of a partner from clinical module
        during a partner will be sync
        :param uuid: unique user identifier by which we can identify the current partner
        :return: list , where 1st index is dob and 2nd index is gender

        """
        authorization = str(self.env['ir.config_parameter'].get_param('base64.authorization'))
        host_unicode_ip = self.env['ir.config_parameter'].search([('key', '=', 'web.base.url')]).value
        extract_ip_with_port = host_unicode_ip[7:]
        extract_ip_without_port = extract_ip_with_port[:-5]
        base_url = 'https://' + extract_ip_without_port + '/openmrs/ws/rest/v1/patientprofile/' + uuid
        header = {'content-type': 'application/json', 'accept': 'application/json', 'catch-control': 'no-cache',
                  'authorization': authorization}
        patient_info = requests.get(base_url, headers=header, verify=False).content
        partner_info_dict = json.loads(str(patient_info))
        dob_string = str(partner_info_dict['patient']['person']['birthdate'])
        index_of_time = dob_string.find('T')
        dob_string = dob_string[:index_of_time]
        dob = datetime.strptime(dob_string, '%Y-%m-%d').date()
        gender = partner_info_dict['patient']['person']['gender']

        return [dob, gender]

    @api.model
    def create(self, vals):
        """This function is extended for get the age and gender of a
        partner, age and gender will assigned whenever partner is created """

        if 'uuid' in vals and vals["uuid"]:
            result = self._get_age_gender(vals["uuid"])
            vals["date_of_birth"] = result[0]
            vals["gender"] = result[1]

        res = super(ResPartner, self).create(vals)
        return res

    @api.multi
    def write(self, vals):
        """This function is extended for get the age and gender of a
        partner, age and gender will assigned in the record if partner has no age or gender"""

        if self.uuid and not self.date_of_birth:
            result = self._get_age_gender(self.uuid)
            vals["date_of_birth"] = result[0]

        if self.uuid and not self.gender:
            result = self._get_age_gender(self.uuid)
            vals["gender"] = result[1]

        res = super(ResPartner, self).write(vals)
        return res

    @api.depends('is_company', 'name', 'parent_id.name',
                 'type', 'company_name', 'ref')
    def _compute_display_name(self):
        diff = dict(show_address=None, show_address_only=None, show_email=None)
        names = dict(self.with_context(**diff).name_get())
        for partner in self:
            partner.display_name = names.get(partner.id)

    @api.depends('date_of_birth')
    def _compute_age(self):
        """
        : This function implemented for realtime calculation of a partner age
        """
        for partner in self:
            if partner.date_of_birth:
                years = relativedelta(datetime.now().date(), datetime.strptime(partner.date_of_birth, '%Y-%m-%d')).years
                months = relativedelta(datetime.now().date(),
                                       datetime.strptime(partner.date_of_birth, '%Y-%m-%d')).months
                days = relativedelta(datetime.now().date(), datetime.strptime(partner.date_of_birth, '%Y-%m-%d')).days
                current_age = str(years) + " " + "Y" + " " + str(months) + " " + "M" + " " + str(days) + " " + "D"
                partner.age = current_age
            else:
                partner.age = False

    # method is overridden to set ref in string returned by name_get
    @api.multi
    def name_get(self):
        res = []
        for partner in self:
            name = partner.name or ''
            if partner.ref:
                name += ' [' + partner.ref + ']'
            if partner.company_name or partner.parent_id:
                if not name and partner.type in ['invoice', 'delivery', 'other']:
                    name = dict(self.fields_get(['type'])['type']['selection'])[partner.type]
                if not partner.is_company:
                    name = "%s, %s" % (partner.commercial_company_name or partner.parent_id.name, name)
            if self._context.get('show_address_only'):
                name = partner._display_address(without_company=True)
            if self._context.get('show_address'):
                name = name + "\n" + partner._display_address(without_company=True)
            name = name.replace('\n\n', '\n')
            name = name.replace('\n\n', '\n')
            if self._context.get('show_email') and partner.email:
                name = "%s <%s>" % (name, partner.email)
            if self._context.get('html_format'):
                name = name.replace('\n', '<br/>')
            res.append((partner.id, name))
        return res

    @api.onchange('village_id')
    def onchange_village_id(self):
        if self.village_id:
            self.district_id = self.village_id.district_id.id
            self.tehsil_id = self.village_id.tehsil_id.id
            self.state_id = self.village_id.state_id.id
            self.country_id = self.village_id.country_id.id
            return {'domain': {'tehsil_id': [('id', '=', self.village_id.tehsil_id.id)],
                               'state_id': [('id', '=', self.village_id.state_id.id)],
                               'district_id': [('id', '=', self.village_id.district_id.id)],
                               'country_id': [('id', '=', self.village_id.country_id.id)]}}
        else:
            return {'domain': {'tehsil_id': [],
                               'state_id': [],
                               'district_id': [],
                               'country_id': []}}


class ResPartnerAttributes(models.Model):
    _name = 'res.partner.attributes'

    partner_id = fields.Many2one('res.partner', string='Partner', required=True, index=True, readonly=False)
    name = fields.Char(string='Name', size=128, required=True)
    value = fields.Char(string='Value', size=128, required=False)
