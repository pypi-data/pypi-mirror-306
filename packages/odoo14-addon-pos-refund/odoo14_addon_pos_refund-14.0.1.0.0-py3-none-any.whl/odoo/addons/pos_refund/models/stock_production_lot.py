# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import api, fields, models
from odoo.tools import float_compare


class ProductionLot(models.Model):
    _inherit = "stock.production.lot"

    available_on_pos = fields.Boolean(compute="_compute_available_on_pos", store=True)

    @api.depends("quant_ids.quantity")
    def _compute_available_on_pos(self):
        for lot in self:
            lot.available_on_pos = (
                float_compare(lot.product_qty, 0, precision_digits=2) > 0
            )

    @api.model
    def get_available_lots(self, product_id, only_available=True):
        lots = []
        product = self.env['product.product'].search([
            ('id', '=', product_id),
            "|",
            ("company_id", "=", self.env.company.id),
            ("company_id", "=", False),            
        ], limit=1)
        if product:
            lots = self.search([
                ("product_id", "=", product.id),
                ("available_on_pos", "=", True)

            ])
            if lots and only_available:
                lots = lots.filtered(lambda a: a.product_qty > 0.0).mapped("name")
        return lots

    @api.model
    def get_used_lots(self, product_id, pos_session=False):
        lots = []
        product = self.env['product.product'].search([
            ('id', '=', product_id),
            "|",
            ("company_id", "=", self.env.company.id),
            ("company_id", "=", False),            
        ], limit=1)
        if product:
            lots = self.search([
                ("product_id", "=", product.id)

            ])
            if product.tracking == 'serial':
                lots = lots.filtered(
                    lambda a: a.product_qty == 0.0
                )
            if pos_session:
                session = False
                session = self.env['pos.session'].search([
                    ('id', '=', pos_session),
                    "|",
                    ("company_id", "=", self.env.company.id),
                    ("company_id", "=", False),       
                ], limit=1)
                if session:
                    pos_lots = session.order_ids.mapped('lines').filtered(
                        lambda a: a.product_id == product.id and a.price_subtotal > 0.0 
                    )
                    if pos_lots and product.tracking == 'serial':
                        pos_lots = pos_lots.filtered(
                            lambda a: a.product_qty == 1.0
                        )
            if lots or pos_lots:
                lots = lots.mapped("name") + pos_lots.mapped('name')
        return lots
