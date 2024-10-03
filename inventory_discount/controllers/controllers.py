# -*- coding: utf-8 -*-
# from odoo import http


# class InventoryDiscount(http.Controller):
#     @http.route('/inventory_discount/inventory_discount', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/inventory_discount/inventory_discount/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('inventory_discount.listing', {
#             'root': '/inventory_discount/inventory_discount',
#             'objects': http.request.env['inventory_discount.inventory_discount'].search([]),
#         })

#     @http.route('/inventory_discount/inventory_discount/objects/<model("inventory_discount.inventory_discount"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('inventory_discount.object', {
#             'object': obj
#         })

