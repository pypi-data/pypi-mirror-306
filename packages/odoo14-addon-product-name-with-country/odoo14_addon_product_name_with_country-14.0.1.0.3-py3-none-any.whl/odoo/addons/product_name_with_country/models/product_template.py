# Copyright 2023 Ángel García de la Chica Herrera <angel.garcia@sygel.es>
# License AGPL-3.0 or later (https://www.gnu.org/licenses/agpl).

from odoo import models, fields, api


class ProductTemplate(models.Model):
    _inherit = "product.template"

    country_id = fields.Many2one(
        comodel_name="res.country",
        string='Country',
    )


class ProductProduct(models.Model):
    _inherit = "product.product"

    def name_get(self):
        result = dict(super().name_get())
        for product in self.sudo().filtered(
                lambda x: x.product_tmpl_id.country_id):
            name = result.get(product.id, False)
            if not self.env.context.get('no_country', False) and name:
                result.update({
                    product.id: "{} ({})".format(
                        name, product.product_tmpl_id.country_id.name)
                })
        return list(result.items())

    @api.model
    def _name_search(self, name, args=None, operator='ilike', limit=100, name_get_uid=None):
        product_ids = super()._name_search(name, args, operator, limit, name_get_uid)
        if name:
            limit_search = limit
            if not limit and product_ids:
                limit_search = len(product_ids)
            elif limit and product_ids:
                limit_search -= len(product_ids)
            if not limit_search or limit_search > 0:
                product_ids += self._search([
                    ('product_tmpl_id.country_id', 'ilike', name),
                    ('id', 'not in', product_ids)
                ], limit=limit_search)
        return product_ids
