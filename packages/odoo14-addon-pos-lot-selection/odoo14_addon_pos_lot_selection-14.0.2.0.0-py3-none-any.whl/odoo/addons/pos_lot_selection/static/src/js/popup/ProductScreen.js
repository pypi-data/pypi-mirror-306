/*
    Copyright 2022 Camptocamp SA (https://www.camptocamp.com).
    License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).
*/
odoo.define("pos_lot_selection.ProductScreen", function (require) {
    "use strict";

    const ProductScreen = require("point_of_sale.ProductScreen");
    const Registries = require("point_of_sale.Registries");
    const NumberBuffer = require("point_of_sale.NumberBuffer");

    const PosLotSaleProductScreen = (ProductScreen) =>
        class extends ProductScreen {
            async _getAddProductOptions(product) {
                if (product.tracking !== "none") {

                    const {confirmed, payload} = await this.showPopup("EditListPopup", {
                        title: this.env._t("Lot/Serial Number(s) Required"),
                        product: product,
                    });

                    // Do not add product if options is undefined.
                    if (!confirmed) return;
                    // Add the product after having the extra information.

                    const modifiedPackLotLines = Object.fromEntries(
                        payload.newArray
                            .filter((item) => item.id)
                            .map((item) => [item.id, item.text])
                    );
                    const newPackLotLines = payload.newArray
                        .filter((item) => !item.id)
                        .map((item) => ({lot_name: item.text}));

                    const draftPackLotLines = {
                        modifiedPackLotLines,
                        newPackLotLines,
                    };
                    this.currentOrder.add_product(product, {
                        draftPackLotLines,
                    });
                    NumberBuffer.reset();
                    return;
                }
                return super._getAddProductOptions(product);
            }
        };

    Registries.Component.extend(ProductScreen, PosLotSaleProductScreen);
    return ProductScreen;
});
