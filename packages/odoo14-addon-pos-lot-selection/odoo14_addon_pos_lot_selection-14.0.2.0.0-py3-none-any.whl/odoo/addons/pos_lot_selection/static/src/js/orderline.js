/*
    Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
odoo.define("pos_lot_selection.orderline", function (require) {
    "use strict";

    var models = require("point_of_sale.models");

    var _super_orderline = models.Orderline.prototype;

    models.Orderline = models.Orderline.extend({
        initialize: function () {
            _super_orderline.initialize.apply(this, arguments);
        },

        can_be_merged_with: function () {
            // Do not merge serial products same as lots
            if (
                this.product.tracking === "serial" &&
                (this.pos.picking_type.use_create_lots ||
                    this.pos.picking_type.use_existing_lots)
            ) {
                return false;
            }
            return _super_orderline.can_be_merged_with.apply(this, arguments);
        },
    });
});
