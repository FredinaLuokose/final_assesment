# -*- coding: utf-8 -*-
# from odoo import http


# class FinalAssesment(http.Controller):
#     @http.route('/final_assesment/final_assesment', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/final_assesment/final_assesment/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('final_assesment.listing', {
#             'root': '/final_assesment/final_assesment',
#             'objects': http.request.env['final_assesment.final_assesment'].search([]),
#         })

#     @http.route('/final_assesment/final_assesment/objects/<model("final_assesment.final_assesment"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('final_assesment.object', {
#             'object': obj
#         })

