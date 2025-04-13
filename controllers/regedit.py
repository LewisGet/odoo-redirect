from odoo import http
from odoo.http import request
from werkzeug.utils import redirect


class RedirectController(http.Controller):
    @http.route('/r/<string:url_name>', type='http', auth='public', website=True)
    def redirect(self, url_name, **kwargs):
        redirect_url = request.env['redirect.url'].sudo().search([('name', '=', url_name)], limit=1)

        log_data = {
            'url_id': None,
            'success': False,
            'ip_address': request.httprequest.remote_addr,
            'user_agent': request.httprequest.user_agent.string,
            'referrer': request.httprequest.referrer
        }

        return_request = request.not_found()

        if redirect_url:
            log_data['url_id'] = redirect_url.id
            log_data['success'] = True
            return_request = request.redirect(redirect_url.target_url)

            if redirect_url.target_url.startswith("http://") or redirect_url.target_url.startswith("https://"):
                return_request = redirect(redirect_url.target_url)

        request.env['redirect.log'].sudo().create(log_data)
        return return_request
