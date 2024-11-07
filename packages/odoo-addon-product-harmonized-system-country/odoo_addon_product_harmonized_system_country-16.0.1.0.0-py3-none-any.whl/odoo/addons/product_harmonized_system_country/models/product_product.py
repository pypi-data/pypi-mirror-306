# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models


class ProductProduct(models.Model):
    _inherit = "product.product"

    def get_hs_local_code_by_country(self, country=False):
        self.ensure_one()
        hs_code = self.get_hs_code_recursively()
        code = ""
        if hs_code and country:
            country_hs_code = hs_code.hs_code_country_ids.filtered(
                lambda a: country.id in a.country_ids.ids
            )
            if len(country_hs_code) == 1:
                code = country_hs_code.local_code
        return code
