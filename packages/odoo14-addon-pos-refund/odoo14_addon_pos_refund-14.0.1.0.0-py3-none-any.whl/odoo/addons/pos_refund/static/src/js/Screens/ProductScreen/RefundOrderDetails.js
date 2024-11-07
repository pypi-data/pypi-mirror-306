odoo.define('point_of_sale.RefundOrderDetails', function(require) {
    'use strict';

    const { _t } = require('web.core');
    const { getDataURLFromFile } = require('web.utils');
    const PosComponent = require('point_of_sale.PosComponent');
    const Registries = require('point_of_sale.Registries');

    class RefundOrderDetails extends PosComponent {
        constructor() {
            super(...arguments);
            const order = this.props;
        }

        getTotal(val) {
            return this.env.pos.format_currency(val);
        }
        getPriceUnit(line) {
            return this.env.pos.format_currency(line.price_unit);
        }
        getSubtotal(line) {
            return this.env.pos.format_currency(line.price_subtotal_incl);
        }
        getPaymentAmount(line){
            return this.env.pos.format_currency(line.amount);
        }
    }
    RefundOrderDetails.template = 'RefundOrderDetails';

    Registries.Component.add(RefundOrderDetails);

    return RefundOrderDetails;
});
