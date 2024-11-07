odoo.define('point_of_sale.RefundOrderLine', function(require) {
    'use strict';

    const { _t } = require('web.core');
    const { getDataURLFromFile } = require('web.utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    var core = require('web.core');

    class RefundOrderLine extends PosComponent {
        constructor(line) {
            super();
            this.id = line.id;
            this.lot = line.pack_lot_ids;
            this.lot_name = line.lot_name;
            this.product_id = line.product_id;
            this.full_product_name = line.full_product_name;
            this.qty = line.qty;
            this.price_unit = line.price_unit;
            this.price_subtotal_incl = line.price_subtotal_incl;
            this.discount = line.discount;
            this.refundedQty = line.refunded_qty;
            this.refund_qty = null;
            this.line = null;
            this.canBeRefunded = line.can_be_refunded;
        }

    };

    RefundOrderLine.template = 'RefundOrderLine';

    Registries.Component.add(RefundOrderLine);

    return RefundOrderLine;
});
