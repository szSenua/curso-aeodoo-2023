from odoo import fields, models

# Defines a new class (model) that represents a database table in Odoo
class HelpdeskTicketAction(models.Model):
    # Technical name of the model used internally by Odoo
    _name = 'helpdesk.ticket.action'
    # Human-readable description of the model
    _description = 'Helpdesk Ticket Action'

    # Actions
    name = fields.Char(
        required=True
    )

    state = fields.Selection([
        ('todo', 'To Do'),
        ('done', 'Done')
        ],
        default = 'todo'
    )

    ticket_id = fields.Many2one(
        'helpdesk.ticket', 
        string='ticket')
    
    def set_done(self):
        self.write({'state':"done"})
    
    def set_todo(self):
        self.write({'state':"todo"})