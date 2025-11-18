from odoo import fields, models

# Defines a new class (model) that represents a database table in Odoo
class HelpdeskTicketTag(models.Model):
    # Technical name of the model used internally by Odoo
    _name = 'helpdesk.ticket.tag'
    # Human-readable description of the model
    _description = 'Helpdesk Ticket Tag'

    # Actions
    name = fields.Char(
        required=True
    )