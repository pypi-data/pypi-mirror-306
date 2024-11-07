# Copyright 2024 Manuel Regidor <manuel.regidor@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo.exceptions import ValidationError
from odoo.tests import common


class TestProductHamonizedSystemCountry(common.TransactionCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.product = cls.env["product.product"].create(
            {
                "name": "Test Product",
            }
        )
        cls.product_categ = cls.env["product.category"].create(
            {"name": "Test category"}
        )
        cls.product_subcateg = cls.env["product.category"].create(
            {"name": "Test subcategory", "parent_id": cls.product_categ.id}
        )
        cls.hs_code = cls.env["hs.code"].create({"local_code": "11111111"})

    def create_hs_code_usa(self, hs_code):
        hs_code.write(
            {
                "hs_code_country_ids": [
                    (
                        0,
                        0,
                        {
                            "country_ids": [self.env.ref("base.us").id],
                            "local_code": "22222222",
                        },
                    ),
                ],
            }
        )

    # Check that HS Code has been properly computed in HS Code country line
    def test_hs_code_country_value(self):
        self.create_hs_code_usa(self.hs_code)
        self.assertEqual(len(self.hs_code.hs_code_country_ids), 1)
        self.assertEqual(self.hs_code.hs_code_country_ids[0].hs_code, "222222")

    # Check that the local HS Code related to a country is returned when the
    # hs.code instance is assigned to the product
    def test_hs_code_in_product(self):
        self.create_hs_code_usa(self.hs_code)
        self.product.write({"hs_code_id": self.hs_code.id})
        local_code = self.product.get_hs_local_code_by_country()
        self.assertFalse(local_code, self.hs_code.local_code)
        local_code = self.product.get_hs_local_code_by_country(self.env.ref("base.us"))
        self.assertEqual(local_code, self.hs_code.hs_code_country_ids[0].local_code)

    # Check that the local HS Code related to a country is returned when the
    # hs.code instance is assigned to the product category or a parent category
    # of the product category
    def test_hs_code_country_in_category(self):
        self.create_hs_code_usa(self.hs_code)
        self.product_subcateg.write({"hs_code_id": self.hs_code.id})
        self.product.write({"categ_id": self.product_subcateg.id})
        local_code = self.product.get_hs_local_code_by_country()
        self.assertFalse(local_code, self.hs_code.local_code)
        local_code = self.product.get_hs_local_code_by_country(self.env.ref("base.us"))
        self.assertEqual(local_code, self.hs_code.hs_code_country_ids[0].local_code)
        self.product.write({"categ_id": self.product_categ.id})
        local_code = self.product.get_hs_local_code_by_country(self.env.ref("base.us"))
        self.assertFalse(local_code, self.hs_code.local_code)
        self.product_categ.write({"hs_code_id": self.hs_code.id})
        local_code = self.product.get_hs_local_code_by_country(self.env.ref("base.us"))
        self.assertEqual(local_code, self.hs_code.hs_code_country_ids[0].local_code)

    # An error occurs when a country is in multiple country HS Code country lines
    # in the same HS Code
    def test_hs_code_in_country_constrain(self):
        with self.assertRaises(ValidationError):
            self.hs_code.write(
                {
                    "hs_code_country_ids": [
                        (
                            0,
                            0,
                            {
                                "country_ids": [
                                    self.env.ref("base.us").id,
                                    self.env.ref("base.be").id,
                                ],
                                "local_code": "22222222",
                            },
                        ),
                        (
                            0,
                            0,
                            {
                                "country_ids": [self.env.ref("base.us").id],
                                "local_code": "33333333",
                            },
                        ),
                    ],
                }
            )
