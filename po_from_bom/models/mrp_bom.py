from odoo import models, fields, api
from odoo.exceptions import UserError

class MrpBom(models.Model):
    _inherit = 'mrp.bom'

    def action_create_purchase_orders(self):
        for bom in self:
            suppliers = {}
            for line in bom.bom_line_ids:
                product = line.product_id
                supplier_info = product.seller_ids
                for supplier in supplier_info:
                    if supplier.partner_id not in suppliers:
                        suppliers[supplier.partner_id] = []
                    suppliers[supplier.partner_id].append(product)

            for supplier, products in suppliers.items():
                purchase_order = self.env['purchase.order'].create({
                    'partner_id': supplier.id,
                    'order_line': [(0, 0, {
                        'product_id': product.id,
                        'product_qty': sum(line.product_qty for line in bom.bom_line_ids if line.product_id == product),
                        'price_unit': product.standard_price,
                    }) for product in products]
                })

    def action_open_customer_wizard(self):
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'select.customer.wizard',
            'view_mode': 'form',
            'target': 'new',
            'context': {'default_user_id': self.id}, 
            }