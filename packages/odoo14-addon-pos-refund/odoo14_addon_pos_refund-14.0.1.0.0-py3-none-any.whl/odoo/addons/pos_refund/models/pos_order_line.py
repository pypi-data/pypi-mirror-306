# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models, api


class PosOrderLine(models.Model):
    _inherit = "pos.order.line"

    lot_name = fields.Char(
        compute="_compute_lot_name",
    )
    refunded_qty = fields.Float(
        string="Refunded Qty."
    )
    can_be_refunded = fields.Boolean(
        compute="_compute_can_be_refunded"
    )

    def _compute_lot_name(self):
        for sel in self:
            lot_name = False
            if sel.pack_lot_ids:
                lot_name = sel.pack_lot_ids[0].lot_name
            sel.lot_name = lot_name

    def _compute_can_be_refunded(self):
        for sel in self:
            sel.can_be_refunded = sel.refunded_qty < sel.qty

    @api.model
    def create(self, values):
        lines = super().create(values)
        if values.get('lineId'):
            line = self.search([
                ('id', '=', values.get('lineId'))
            ], limit=1)
            if line:
                line.refunded_qty += -1 * values.get('qty')
        return lines
            