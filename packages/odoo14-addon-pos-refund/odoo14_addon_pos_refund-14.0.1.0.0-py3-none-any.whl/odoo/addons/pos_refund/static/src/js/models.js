odoo.define('pos_refund.order', function (require) {
    "use strict";

var models = require('point_of_sale.models');
var super_order_model = models.Order.prototype;
var super_orderline = models.Orderline.prototype;

models.Order = models.Order.extend({

    add_product: function(product, options){
        super_order_model.add_product.apply(this, arguments);
        var line = this.get_last_orderline()
        if (options.lineId != undefined){
            line.lineId = options.lineId;
        }
    },
    export_as_JSON: function () {
        const json = super_order_model.export_as_JSON.apply(this, arguments);
    	if (this.refundOrder){
    		json['refundOrder'] = this.refundOrder.id;
    	}
        return json;
    },
});

models.Orderline = models.Orderline.extend({
    export_as_JSON: function () {
        const json = super_orderline.export_as_JSON.apply(this, arguments);
        if (this.lineId){
            json['lineId'] = this.lineId;
        }
        return json;
    },
});

});
