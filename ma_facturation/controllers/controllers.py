# -*- coding: utf-8 -*-
# from odoo import http


# class MaFacturation(http.Controller):
#     @http.route('/ma_facturation/ma_facturation', auth='public')
#     def index(self, **kw):
#         return "Hello, world"

#     @http.route('/ma_facturation/ma_facturation/objects', auth='public')
#     def list(self, **kw):
#         return http.request.render('ma_facturation.listing', {
#             'root': '/ma_facturation/ma_facturation',
#             'objects': http.request.env['ma_facturation.ma_facturation'].search([]),
#         })

#     @http.route('/ma_facturation/ma_facturation/objects/<model("ma_facturation.ma_facturation"):obj>', auth='public')
#     def object(self, obj, **kw):
#         return http.request.render('ma_facturation.object', {
#             'object': obj
#         })
