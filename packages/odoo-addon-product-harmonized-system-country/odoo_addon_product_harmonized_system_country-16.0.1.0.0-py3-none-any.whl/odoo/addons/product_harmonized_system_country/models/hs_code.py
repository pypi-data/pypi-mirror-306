# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import fields, models


class HSCode(models.Model):
    _inherit = "hs.code"

    hs_code_country_ids = fields.One2many(
        string="H.S. Countries",
        comodel_name="hs.code.country",
        inverse_name="hs_code_id",
    )
