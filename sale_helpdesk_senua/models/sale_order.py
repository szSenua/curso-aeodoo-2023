from odoo import models, api, fields, _

class SaleOrder(models.Model):
    _inherit = "sale.order"
# - Añadir un listado de tickets en el pedido de venta.
    ticket_ids = fields.One2many("helpdesk.ticket", "sale_order_id", string="Tickets")
# - Añadir el campo etiqueta de helpdesk en el producto y poner un botón que cree un ticket desde los pedidos utilizando las etiquetas de los productos del pedido.
    def create_ticket_from_sale_order(self):
        self.ensure_one()
        self.env['helpdesk.ticket'].create({
            'name': self.name,
            'person_id': self.partner_id.id,  # Corregido: era 'person_id'
            'tag_ids': [(6, 0, self.order_line.mapped('product_id.helpdesk_tag_id').ids)],
            'sale_order_id': self.id,
        })


# - Hacer que, al cancelar un pedido, se cancelen todos los tickets asociados. (Volver a poner el campo state como un selection).
    def _action_cancel(self):
        self.ticket_ids.write({
            'state': 'canceled'
        })
        return super()._action_cancel()