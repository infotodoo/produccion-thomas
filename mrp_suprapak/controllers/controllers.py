# -*- coding: utf-8 -*-
# from odoo import http


# class SuprapakMrp(http.Controller):
#     @http.route('/mrp_suprapak/mrp_suprapak/', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/mrp_suprapak/mrp_suprapak/objects/', auth='public')
#     def list(self, **kw):
#         return http.request.render('mrp_suprapak.listing', {
#             'root': '/mrp_suprapak/mrp_suprapak',
#             'objects': http.request.env['mrp_suprapak.mrp_suprapak'].search([]),
#         })

#     @http.route('/mrp_suprapak/mrp_suprapak/objects/<model("mrp_suprapak.mrp_suprapak"):obj>/', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('mrp_suprapak.object', {
#             'object': obj
#         })
