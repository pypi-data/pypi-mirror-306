# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import _, api, fields, models
from odoo.exceptions import ValidationError


class HSCodeCountry(models.Model):
    _name = "hs.code.country"
    _description = "H.S. Code Country"

    country_ids = fields.Many2many(
        string="Countries",
        comodel_name="res.country",
    )
    local_code = fields.Char(
        required=True,
    )
    hs_code = fields.Char(
        string="H.S. Code",
        compute="_compute_hs_code",
        store=True,
        precompute=True,
    )
    hs_code_id = fields.Many2one(
        string="H.S. Code",
        comodel_name="hs.code",
        ondelete="cascade",
    )

    @api.constrains("country_ids")
    def _check_country_ids(self):
        for hs_code_country in self:
            other_prod_hs_code_countries = (
                hs_code_country.hs_code_id.hs_code_country_ids - hs_code_country
            )
            if set(hs_code_country.country_ids.ids) & set(
                other_prod_hs_code_countries.country_ids.ids
            ):
                raise ValidationError(
                    _("Some countries are already in another H.S. Code country line.")
                )

    @api.depends("local_code")
    def _compute_hs_code(self):
        for hs_code in self:
            hs_code.hs_code = hs_code.local_code and hs_code.local_code[:6]
