# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).


from odoo import fields, models, api, _


class PosOrder(models.Model):
    _inherit = "pos.order"

    refunded_by_ids = fields.One2many(
        comodel_name="pos.order",
        inverse_name="refund_id",
        readonly=True
    )
    refund_id = fields.Many2one(
        comodel_name="pos.order",
        readonly=True
    )
    refunded_by_count = fields.Integer(
        compute='_compute_refunded_by_count'
    )

    def _compute_refunded_by_count(self):
        for sel in self:
            sel.refunded_by_count = len(sel.refunded_by_ids)

    @api.model
    def _order_fields(self, ui_order):
        fields = super()._order_fields(ui_order)
        if ui_order.get('refundOrder'):
            fields['refund_id'] = ui_order.get('refundOrder')
        return fields

    @api.model
    def create_from_ui(self, orders, draft=False):
        
        new_orders = super().create_from_ui(orders, draft)

        for order in new_orders:
            order_id = self.browse(order.get('id'))
            if order_id and order_id.refund_id:
                refunds_no = len(order_id.refund_id.refunded_by_ids)
                order_id.write({
                    'name': order_id.refund_id.name + _('REFUND') + '/' + str(refunds_no)
                })

        for order in orders:
            lines = list(filter(lambda a: a[2].get('lineId'), orders[0].get('data').get('lines')))
            for line in lines:
                order_line = self.env['pos.order.line'].search([
                    ('id', '=', line[2].get('lineId'))
                ], limit=1)
                order_line.write({
                    'refunded_qty': order_line.refunded_qty + (-1 * line[2].get('qty'))
                })
        return new_orders

    def action_refunded_by(self):
        self.ensure_one()
        return {
            'name': _('Orders'),
            'res_model': 'pos.order',
            'view_mode': 'tree,form',
            'views': [
                (self.env.ref('point_of_sale.view_pos_order_tree_no_session_id').id, 'tree'),
                (self.env.ref('point_of_sale.view_pos_pos_form').id, 'form'),
                ],
            'type': 'ir.actions.act_window',
            'domain': [('id', 'in', self.refunded_by_ids.ids)],
        }
