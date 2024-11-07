# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

{
    "name": "Product Harmonized System Country",
    "summary": "Specific HS Code for given countries",
    "version": "16.0.1.0.0",
    "category": "Product",
    "website": "https://github.com/sygel-technology/sy-intrastat-extrastat",
    "author": "Sygel, Odoo Community Association (OCA)",
    "license": "AGPL-3",
    "application": False,
    "installable": True,
    "depends": [
        "product_harmonized_system",
    ],
    "data": [
        "security/ir.model.access.csv",
        "views/hs_code.xml",
    ],
}
