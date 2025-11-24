from odoo import api, fields, models

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

    # Many to many field
    ticket_ids = fields.Many2many(
        'helpdesk.ticket',
        relation='helpdesk_ticket_tag_rel',
        column1='tag_id',
        column2='ticket_id',
        string='Tickets')
    
    @api.model
    def _clean_tags(self):
        tags = self.search([('ticket_ids', '=', False)])
        tags.unlink()