odoo.define('pos_refund.PosRefundButton', function(require) {
    'use strict';

    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    class PosRefundButton extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click', this.onClick);
        }
        get refundOrder(){
            var name = false;
            var order = this.env.pos.get_order();
            if (order && order.refundOrder != undefined) {
                name = order.refundOrder.name;
            }
            return name;
        }
        async onClick() {
            this.showScreen('PosRefundScreen');
        }
    }
    PosRefundButton.template = 'PosRefundButton';

    ProductScreen.addControlButton({
        component: PosRefundButton,
        condition: function() {
            return true;
        },
    });

    Registries.Component.add(PosRefundButton);

    return PosRefundButton;
});
