from odoo import http
from odoo.http import request
from werkzeug.urls import url_parse
from werkzeug.utils import redirect
from werkzeug.wrappers import Response

import requests as pull


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

            to_url = redirect_url.target_url

            if to_url.startswith(("http://", "https://")):
                return_request = redirect(redirect_url.target_url)

            if self.is_image_url(to_url):
                return_request = self.get_image_request(to_url)


        request.env['redirect.log'].sudo().create(log_data)
        return return_request

    def is_image_url(self, url):
        parsed_url = url_parse(url.lower())
        return parsed_url.path.endswith((".jpg", ".jpeg", ".png", ".gif", ".bmp", ".webp", ".svg"))

    def get_image_request(self, url):
        try:
            image_request = pull.get(url, timeout=5, stream=True)
            image_request.raise_for_status() # 400,500

            content_type = image_request.headers.get("Content-Type")

            if not content_type or not content_type.startswith("image/"):
                raise BaseException("get content type fail")

        except pull.exceptions.RequestException as e:
            return redirect(url)

        return Response(
            image_request.content,
            headers=[('Content-Type', content_type)]
        )
