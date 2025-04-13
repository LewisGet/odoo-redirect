from odoo import models, fields


class RedirectLog(models.Model):
    _name = 'redirect.log'
    _description = 'Redirect Log'

    url_id = fields.Many2one('redirect.url', string='Redirect URL', required=False)
    success = fields.Boolean(string='Success', default=False)
    ip_address = fields.Char(string='IP Address')
    user_agent = fields.Char(string='User agent')
    referrer = fields.Char(string='Referrer')
    timestamp = fields.Datetime(string='Timestamp', default=fields.Datetime.now)
