odoo.define('pos_refund.PosRefundScreen', function(require) {
    'use strict';

    const { Gui } = require('point_of_sale.Gui');
    const { debounce } = owl.utils;
    const PosComponent = require('point_of_sale.PosComponent');
    const ProductScreen = require('point_of_sale.ProductScreen');
    const { useListener } = require('web.custom_hooks');
    const Registries = require('point_of_sale.Registries');

    var RefundOrderLine = require('point_of_sale.RefundOrderLine');
    var models = require('point_of_sale.models');
    var _super_orderline = models.Orderline.prototype;

    class PosRefundScreen extends PosComponent {
        constructor() {
            super(...arguments);
            useListener('click-refund', () => this.refund());
            this.state = {
                // selectedClient: this.props.client,
                detailIsShown: false,
                refundOrder : this.props.order,
                // isEditMode: false,
                detailsProps: {
                    selectedOrder: this.props.order,
                    selectedOrderLines: [],
                    paymentLines: [],
                },
            };
        }

        back() {
            this.trigger('close-temp-screen');
        }

        refundVals(){
            var rightVal = false
            var refundVals = $("#refund_lines .refund_qty").each(function(){
                if (parseFloat(this.value) > 0.0){
                    rightVal = true
                }
            });
            return rightVal
        }

        checkQty(){
            var self = this;
            var rightQty = true
            $("#refund_lines .refund_qty").each(function(){
                var line = self.state.detailsProps.selectedOrderLines.filter(l => l.id == this.getAttribute('line_id'));
                if (parseFloat(this.value) + line[0].refundedQty > line[0].qty){
                    rightQty = false
                    Gui.showPopup('ErrorPopup', {
                        title: 'Invalid quantities',
                        body: 'Make sure that the product quantity selected can be refunded',
                    });                    
                }else if(isNaN(this.value) | parseFloat(this.value) < 0){
                    rightQty = false
                    Gui.showPopup('ErrorPopup', {
                        title: 'Invalid quantities',
                        body: 'Only positive numbers are valid.',
                    });
                }
            })
            return rightQty;
        }

        async refund(){
            var rightQty = this.checkQty();
            if (rightQty){
                var refund_vals = this.refundVals();
                if (refund_vals){
                    var create_new_order = this.env.pos.get_order_list().length != 1
                    this.env.pos.delete_current_order();

                    if (create_new_order){
                        var order = this.env.pos.add_new_order();
                    }else{
                        var order = this.env.pos.get_order();
                    }

                    // Set customer if defined
                    if (this.state.detailsProps.selectedOrder.partner_id != false){
                        var client = this.env.pos.db.get_partner_by_id(this.state.detailsProps.selectedOrder.partner_id[0])
                        order.set_client(client)
                    }
                    // Set refund order
                    order.refundOrder = this.state.detailsProps.selectedOrder;

                    var self = this;
                    $("#refund_lines .refund_qty").each(function(){
                        if (this.value && parseFloat(this.value) > 0.0){
                            var line = self.state.detailsProps.selectedOrderLines.filter(l => l.id == this.getAttribute('line_id'));
                            if (line){
                                var product  = self.env.pos.db.get_product_by_id(line[0].product_id[0])
                                var line = line[0]
                                var options = {
                                    quantity:-1*this.value,
                                    price:line.price_unit,
                                    lineId: this.getAttribute('line_id'),
                                }
                                if (line.lot_name != false){
                                    var modifiedPackLotLines = {}
                                    var newPackLotLines = [{lot_name:line.lot_name}]
                                    options['draftPackLotLines'] = {
                                        modifiedPackLotLines,
                                        newPackLotLines
                                    }
                                }
                                order.refundOrder = self.state.detailsProps.selectedOrder;
                                order.add_product(product, options);                        
                            }
                        }

                    });
                }
                this.showScreen('ProductScreen');             
            }
        }

        searchOrder(event) {
            var self = this;
            self.rpc({
                model: 'pos.order',
                method: 'search_read',
                kwargs: {
                    domain: ['|', 
                        ['name', '=', event.target.value.trim()],
                        ['l10n_es_unique_id', '=', event.target.value.trim()],
                    ],
                    fields: ['id', 'name', 'amount_total', 'date_order', 'user_id', 'lines', 'partner_id'],
                },
            }).then(function(order) {
                if (!order.length){
                    self.state.detailIsShown = false;
                    event.target.style = "border: solid red 3px;";
                    self.render();
                }else{
                    self.state.detailIsShown = true;
                    self.state.detailsProps.selectedOrder = order[0];
                    self.rpc({
                        model: 'pos.order.line',
                        method: 'search_read',
                        kwargs: {
                            domain: [['id', 'in', order[0].lines]],
                            fields: ['id', 'product_id', 'full_product_name', 'qty', 'price_unit', 'price_subtotal_incl', 'discount', 'pack_lot_ids', 'lot_name', 'refunded_qty', 'can_be_refunded'],
                        },
                    }).then(function(lines) {
                        event.target.style = "border: solid green 3px;";            
                        // self.state.detailsProps.selectedOrderLines = lines;

                        var refundLines = []
                        lines.forEach(function (line) {
                            // orderline.remove_orderline()
                            refundLines.push(new RefundOrderLine(line));
                        });
                        self.state.detailsProps.selectedOrderLines = refundLines;         
                        self.rpc({
                            model: 'pos.payment',
                            method: 'search_read',
                            kwargs: {
                                domain: [['pos_order_id', '=', order[0].id]],
                                fields: ['id', 'amount', 'payment_method_id'],
                            },                         
                        }).then(function(payments) {
                            self.state.detailsProps.paymentLines = payments;
                            self.render();
                        })
                        
                    })
                }
            });
        }
    }

    PosRefundScreen.template = 'PosRefundScreen';

    Registries.Component.add(PosRefundScreen);

    return PosRefundScreen;
});
