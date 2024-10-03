# -*- coding: utf-8 -*-
# from odoo import http


# class InvoiceRivision(http.Controller):
#     @http.route('/invoice_rivision/invoice_rivision', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/invoice_rivision/invoice_rivision/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('invoice_rivision.listing', {
#             'root': '/invoice_rivision/invoice_rivision',
#             'objects': http.request.env['invoice_rivision.invoice_rivision'].search([]),
#         })

#     @http.route('/invoice_rivision/invoice_rivision/objects/<model("invoice_rivision.invoice_rivision"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('invoice_rivision.object', {
#             'object': obj
#         })

