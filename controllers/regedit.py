from odoo import http
from odoo.http import request


class RedirectController(http.Controller):
    @http.route('/r/<string:url_name>', type='http', auth='public', website=True)
    def redirect(self, url_name, **kwargs):
        redirect_url = request.env['redirect.url'].sudo().search([('name', '=', url_name)], limit=1)

        log_data = {
            'url_id': None,
            'success': False,
            'ip_address': request.httprequest.remote_addr,
        }

        return_request = request.not_found()

        if redirect_url:
            log_data['url_id'] = redirect_url.id
            log_data['success'] = True
            return_request = request.redirect(redirect_url.target_url)

        request.env['redirect.log'].sudo().create(log_data)
        return return_request
