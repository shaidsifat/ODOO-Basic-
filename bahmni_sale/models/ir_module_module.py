from odoo import api,models

class Module(models.Model):
    _inherit = "ir.module.module"

    @api.multi
    def button_immediate_upgrade(self):
        """
        : This function is extended for create a key named as 'base64.authorization' in system parameters and add a
        base64 formatted clinical username and password as value
        """
        res = super(Module, self).button_immediate_upgrade()
        config_param = self.env['ir.config_parameter'].search([('key','=','base64.authorization')])
        if not config_param:
            self.env['ir.config_parameter'].create({"key":"base64.authorization","value":""})
        return res