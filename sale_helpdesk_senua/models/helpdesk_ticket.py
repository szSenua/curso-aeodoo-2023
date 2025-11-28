from odoo import models, api, fields, _

class HelpdeskTicket(models.Model):
    # This means we are extending the existing helpdesk.ticket model
    _inherit = "helpdesk.ticket"
    # Adding a Many2one field to link the ticket to a sale order
    sale_order_id = fields.Many2one("sale.order", string="Sale Order")
