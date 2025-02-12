from odoo import models, fields, api
from odoo.exceptions import UserError

class SelectCustomerWizard(models.TransientModel):
    _name = 'select.customer.wizard'
    _description = 'Select Customer Wizard'

    customer_id = fields.Many2one('res.partner', string='Customer', required=True)
    bom_id = fields.Many2one('mrp.bom', string='BOM')

    def action_create_delivery_order(self):

        if not self.customer_id:
            raise UserError("Please select a customer.")

        # Get the components from the context (assumed to be passed when opening the wizard)
        bom_components = self.bom_id.bom_line_ids
        if not bom_components:
            raise UserError("No components found to create a delivery order.")

        # Create the delivery order
        delivery_order = self.env['stock.picking'].create({
            'partner_id': self.customer_id.id,
            'picking_type_id': self.env.ref('stock.picking_type_out').id,
            'move_lines': [(0, 0, {
                'product_id': component.product_id.id,
                'product_uom_qty': component.product_qty,
                'product_uom': component.product_id.uom_id.id,
            }) for component in bom_components],
        })

        return {
            'type': 'ir.actions.act_window',
            'res_model': 'stock.picking',
            'res_id': delivery_order.id,
            'view_mode': 'form',
            'target': 'current',
        }