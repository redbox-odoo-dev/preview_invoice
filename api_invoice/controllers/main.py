# -*- coding:utf-8 -*-
import json
from odoo import http
from odoo.http import request, Response



class Invoice(http.Controller):
    @http.route('/preview/invoice', methods=['GET'], csrf=False, type='http', auth="public", website=True)
    def get_invoice(self, **kw):
        if kw and kw['inv_id']:
            inv_id = kw['inv_id']
            report = request.env['ir.actions.report'].sudo()
            pdf = report._render_qweb_pdf(report_ref='account.report_invoice_with_payments', res_ids=int(inv_id), data=None)[0]
            pdfhttpheaders = [('Content-Type', 'application/pdf'), ('Content-Length', len(pdf))]
            response = Response(pdf, headers=pdfhttpheaders)
            response.headers.add('status', True)
            return response
        else:
            response = [{'status':False,'error':'missing inv_id'}]
            return json.dumps(response)
