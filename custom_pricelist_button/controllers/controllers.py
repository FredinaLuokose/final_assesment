# -*- coding: utf-8 -*-
# from odoo import http


# class CustomPricelistButton(http.Controller):
#     @http.route('/custom_pricelist_button/custom_pricelist_button', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/custom_pricelist_button/custom_pricelist_button/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('custom_pricelist_button.listing', {
#             'root': '/custom_pricelist_button/custom_pricelist_button',
#             'objects': http.request.env['custom_pricelist_button.custom_pricelist_button'].search([]),
#         })

#     @http.route('/custom_pricelist_button/custom_pricelist_button/objects/<model("custom_pricelist_button.custom_pricelist_button"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('custom_pricelist_button.object', {
#             'object': obj
#         })

