# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import ValidationError


class MaFacturation(models.Model):
    _name = 'ma.facturation'
    _rec_name = "ref"
    _description = 'Ma facturation'

    ref = fields.Char('Reference facture')
    customers_id = fields.Many2one(comodel_name='customer.customer', string='Client', required=True)
    date = fields.Datetime(string="Date de facturation", required=True, readonly=False, default=fields.Datetime.now)
    order_line_ids = fields.One2many(comodel_name='order.line', inverse_name='facturation_id', string="Ligne de commande",)
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id,
                                  required=True)
    amount_cumul = fields.Monetary(string="Montant total", compute="_cumul_total", readonly=True)
    state = fields.Selection(string="Statut",
                                        selection=[('new', 'Nouveau'), ('done', 'Validé'), ('cancel', 'Annulé')],
                                        default='new', readonly=True)

    @api.model
    def create(self, values):
        values['ref'] = self.env['ir.sequence'].next_by_code('ma.facturation')
        return super(MaFacturation, self).create(values)

    @api.depends('order_line_ids')
    def _cumul_total(self):
        for rec in self:
            if rec.state == 'cancel':
                rec.amount_cumul = 0
            else:
                rec.amount_cumul = sum(rec.order_line_ids.mapped('total'))



    @api.constrains('order_line_ids')
    def _check_field(self):
        for rec in self:
            if not rec.order_line_ids :
                raise ValidationError("Veuillez ajouter un article")

    def action_new(self):
        for rec in self:
            rec.state = 'new'

    def action_done(self):
        for rec in self:
            if rec.state != 'cancel':
                rec.state = 'done'

    def action_cancel(self):
        for rec in self:
            if rec.state == 'done':
                rec.state = 'cancel'


class OrderLine(models.Model):
    _name = 'order.line'
    _description = "ligne de commande"

    facturation_id = fields.Many2one(comodel_name='ma.facturation', string='Client', required=False)
    article_id = fields.Many2one(comodel_name='product.template', string='Article', required=False)
    price = fields.Float(string="Prix", related="article_id.list_price")
    quantity = fields.Integer(string='Quantité', required=True)
    total = fields.Monetary(string="Total", store=True, currency_field='currency_id', tracking=True, compute='compute_total_amount')
    currency_id = fields.Many2one('res.currency', string='Devise', default=lambda self: self.env.company.currency_id,
                                  required=True)

    @api.depends('quantity')
    def compute_total_amount(self):
        for rec in self:
            if rec.quantity:
                rec.total = rec.price * rec.quantity

    @api.constrains('quantity')
    def _check_field(self):
        for rec in self:
            if rec.quantity == 0:
                raise ValidationError("Veuillez ajouter la quantité de l'article s'il vous plait ! ")


class ResPartner(models.Model):
    _name = 'res.partner'
    _inherit = 'res.partner'

    customer = fields.Boolean(string='Client', required=False)


class Customer(models.Model):
    _name = 'customer.customer'
    _rec_name = "res_id"

    res_id = fields.Many2one(comodel_name='res.partner', string="Client", domain="[('customer', '=', False)]",
                             required=True)
    image = fields.Binary(string="Image", related="res_id.image_1920", readonly=False)
    phone = fields.Char(string="Téléphone", related="res_id.phone", readonly=False)
    mobile = fields.Char(string="Mobile", related="res_id.mobile", readonly=False)
    street = fields.Char(string="Rue", related="res_id.street", readonly=False)
    city = fields.Char(string="Ville", related="res_id.city", readonly=False)
    bill_ids = fields.One2many(comodel_name='ma.facturation', inverse_name='customers_id', string='Factures')

    def _update_is_selected(self):
        """
         contact become a customer
        @return:
        """
        if self.res_id:
            self.res_id.customer = True

    @api.model
    def create(self, vals):
        """
        Creates a customer if the boolean selected is True
        @param vals:
        @return:
        """
        record = super(Customer, self).create(vals)
        record._update_is_selected()
        return record

    def unlink(self):
        """
        Verify and update contact
        @return:
        """
        for record in self:
            if record.res_id:
                record.res_id.customer = False
        return super().unlink()
