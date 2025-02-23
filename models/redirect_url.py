from odoo import models, fields


class RedirectURL(models.Model):
    _name = 'redirect.url'
    _description = 'Redirect URL'

    name = fields.Char(string='Name', required=True)
    target_url = fields.Char(string='Target URL', required=True)
