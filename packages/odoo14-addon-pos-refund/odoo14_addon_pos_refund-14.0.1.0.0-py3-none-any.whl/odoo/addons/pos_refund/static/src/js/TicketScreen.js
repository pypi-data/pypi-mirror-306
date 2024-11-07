odoo.define('pos_refund.TicketScreen', function (require) {
    'use strict';

    const TicketScreen = require('point_of_sale.TicketScreen');
    const Registries = require('point_of_sale.Registries');

    const PosRefundScreen = (TicketScreen) =>
        class extends TicketScreen {
            getRefund(order) {
                return order.refundOrder ? order.refundOrder.name : '';
            }
        }

    Registries.Component.extend(TicketScreen, PosRefundScreen);

    return PosRefundScreen;
})
