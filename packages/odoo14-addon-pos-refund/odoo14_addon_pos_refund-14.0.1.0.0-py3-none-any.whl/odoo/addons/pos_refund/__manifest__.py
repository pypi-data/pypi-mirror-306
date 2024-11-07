# Copyright 2022 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "POS Refund",
    "version": "14.0.1.0.0",
    "category": "Point of Sale",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "depends": [
        "point_of_sale",
        "l10n_es_pos",
    ],
    'data': [
        'views/assets.xml',
        'views/pos_order_view.xml',
    ],
    'qweb': [
        "static/src/xml/PosRefundButton.xml",
        "static/src/xml/TicketScreen.xml",
        "static/src/xml/PosRefundScreen.xml",
        "static/src/xml/RefundOrderDetails.xml",
        "static/src/xml/RefundOrderLine.xml",
    ],
    "application": False,
    "installable": True,
}
