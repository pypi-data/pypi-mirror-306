/*
    Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
odoo.define("pos_lot_selection.LotSelectorPopup", function (require) {
    "use strict";

    const Registries = require("point_of_sale.Registries");
    const EditListPopup = require("point_of_sale.EditListPopup");

    var models = require('point_of_sale.models');
    var _super_order = models.Order.prototype;
    var serialLot = undefined;
    var realTimeUpdateStock;

    const LotSelectorPopup = (EditListPopup) =>

        class extends EditListPopup {

            getPayload() {
                var serialLot = undefined
                if (this.serialLot != undefined){
                    serialLot = this.serialLot;
                }else{
                    serialLot = $("#new_select").val();
                }
                return {
                    newArray: [Object.assign({}, {text: serialLot})],
                };
            }

            async isRealTimeUpdateStock(){
                var updateStock = await this.rpc(
                    {
                        model: "res.company",
                        method: "search_read",
                        kwargs: {
                            domain: [
                                ["id", "=", this.env.session.company_id],
                            ],
                            fields: ["point_of_sale_update_stock_quantities"],
                        },
                        context: {...this.env.session.user_context},
                    },
                    // el shadow: true evita que salga un spinner
                    {shadow: true}
                )
                return updateStock[0].point_of_sale_update_stock_quantities;
            }

            async lotExists(){
                var lotExists = false
                var payload = this.getPayload()
                var product = this.props.product
                if (payload && payload.newArray.length == 1 && payload.newArray[0].text){
                    var serialLot = payload.newArray[0].text
                    payload = payload.newArray[0].text
                    var lots_no = await this.rpc(
                        {
                            model: "stock.production.lot",
                            method: "search_count",
                            args: [[
                                "&",
                                "&",
                                ["product_id", "=", this.props.product.id],
                                ["name", "=", serialLot],
                                "|",
                                ["company_id", "=", this.env.pos.company.id],
                                ["company_id", "=", false],
                            ]],
                            context: {...this.env.session.user_context},
                        },
                        {shadow: true}
                    );
                    if (lots_no == 1){
                        lotExists = true
                    }
                }
            return lotExists
            }

            sessionQtyOngoing(){
                var productId = this.props.product.id
                var qty = 0.0
                var serialLot = this.getPayload().newArray[0].text
                this.env.pos.get_order_list().forEach(function(order, index) {
                    order.orderlines.forEach(function(line, index) {
                        if (line.product && line.product.id == productId && line.pack_lot_lines){
                            line.pack_lot_lines.get_valid_lots().forEach(function(lot, index){
                                if (lot.attributes.lot_name == serialLot){
                                    qty += line.quantity
                                }
                            });
                        }
                    });
                });
                return qty
            }

            async sessionQtyCompleted(){
                var qty = 0.0;
                if (this.realTimeUpdateStock != 'real'){
                    qty = await this.rpc(
                        {
                            model: "pos.session",
                            method: "open_session_lot_serial_amount",
                            args: [
                                this.props.product.id,
                                this.getPayload().newArray[0].text
                            ],
                            context: {...this.env.session.user_context},
                        },
                        // el shadow: true evita que salga un spinner
                        {shadow: true}
                    );                    
                }

                return qty
            }

            async lotStockQty(){
                var qty = 0.0
                var qtyRet = await this.rpc(
                    {
                        model: "product.product",
                        method: "search_read",
                        kwargs: {
                            domain: [
                                ["id", "=", this.props.product.id],
                            ],
                            fields: ["qty_available"],
                        },
                        context: { lot_id: this.getPayload().newArray[0].text, company_id: this.env.pos.company.id },
                    },
                    // el shadow: true evita que salga un spinner
                    {shadow: true}
                );
                if (qtyRet && qtyRet.length == 1){
                    qty = qtyRet[0]['qty_available']
                }
                return qty
            }

            async qtyBalance(){
                var lotStockQty = await this.lotStockQty()
                var sessionQtyCompleted = await this.sessionQtyCompleted()
                var sessionQtyOngoing = this.sessionQtyOngoing()
                return lotStockQty - sessionQtyCompleted - sessionQtyOngoing
            }

            async canBeAdded(){
                var canBeAdded = false
                var lotExists = await this.lotExists()
                if (lotExists){
                    var qtyBalance = await this.qtyBalance()
                    var operationType = document.getElementById('operation_type').value
                    var productTrackingPolicy = this.props.product.tracking
                    if (operationType == 'sale' && ((productTrackingPolicy == 'serial' && qtyBalance == 1.0)) | (productTrackingPolicy == 'lot' && qtyBalance >= 1.0)){
                        canBeAdded = true
                    }else if (operationType == 'refund' && ((productTrackingPolicy == 'serial' && qtyBalance == 0.0) | (productTrackingPolicy == 'lot'))){
                        canBeAdded = true
                    }
                }
                return canBeAdded
            }

            async confirm() {                
                var canProcede = true
                var connectionStatus = this.env.pos.get('synch').status
                if (connectionStatus == 'connected'){
                    this.serialLot = $("#new_select").val();
                    this.realTimeUpdateStock = await this.isRealTimeUpdateStock().catch(() => Promise.resolve("ERROR"));
                    canProcede = await this.canBeAdded().catch(() => Promise.resolve("ERROR"))
                    if (canProcede == "ERROR" || this.realTimeUpdateStock == "ERROR"){
                        await this.showPopup('OfflineErrorPopup', {
                            title: this.env._t('Something went wrong.'),
                            body:
                                this.env._t('The serial number/lot could not be checked, so the product was added. Please, check your Internet connection.'),
                        });
                    }
                }
                if (!canProcede){
                    var inputText = document.getElementById('new_select');
                    if (inputText){
                        inputText.style = "border: solid red 3px;";
                    }                   
                }else{
                    super.confirm()
                } 
            }
        };

    Registries.Component.extend(EditListPopup, LotSelectorPopup);
    return EditListPopup;
});
