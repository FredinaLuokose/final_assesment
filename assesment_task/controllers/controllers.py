# -*- coding: utf-8 -*-
# from odoo import http


# class AssesmentTask(http.Controller):
#     @http.route('/assesment_task/assesment_task', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/assesment_task/assesment_task/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('assesment_task.listing', {
#             'root': '/assesment_task/assesment_task',
#             'objects': http.request.env['assesment_task.assesment_task'].search([]),
#         })

#     @http.route('/assesment_task/assesment_task/objects/<model("assesment_task.assesment_task"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('assesment_task.object', {
#             'object': obj
#         })

