from odoo import _, api, fields, models

# - Crear un asistente para crear tickets desde la etiqueta, que coja por contexto el active_id para 
# que el ticket creado tenga asociada la etiqueta desde la que se lanza el asistente.
# - Crear el botón en el formulario de la etiqueta y después de crear el ticket redirigir al ticket creado

class HelpdeskCreateTicket(models.TransientModel):
    # Wizard to create Helpdesk Ticket
    # The wizard has two steps:
    # Step 1: Fill in the ticket details (name, description)
    # Step 2: View the created ticket
    # The tag is pre-filled from the context (active_id)
    # After creating the ticket, the wizard shows a button to view the created ticket
    # The ticket is linked to the tag selected when launching the wizard
    # The wizard uses a invisible field 'state' to manage the steps
    
    _name = "helpdesk.create.ticket" # Wizard model name
    _description = "Helpdesk Create Ticket Wizard" # Wizard model description
    
    # Fields
    tag_id = fields.Many2one(
        "helpdesk.ticket.tag", 
        string="Tag", 
        default=lambda self: self.env.context.get("active_id") or False
    )
    # State field to manage the wizard steps
    state = fields.Selection(
        [
            ('step_1', 'Step 1'),
            ('step_2', 'Step 2'),
        ],
        string='State',
        default='step_1',
    )
    # Ticket details fields
    name = fields.Char(string="Name", required=True) # Ticket name
    description = fields.Text(string="Description") # Ticket description
    # Field to store the created ticket
    ticket_id = fields.Many2one(
        'helpdesk.ticket',
        string='Ticket',
        )

    
    @api.model
    def default_get(self, fields):
         # Override default_get to fill tag_id from the context
        res = super().default_get(fields)
        if self.env.context.get("active_id"):
            res["tag_id"] = self.env.context["active_id"]
        return res
    
    def create_ticket(self):
        # Create the ticket with the data entered in the wizard
        self.ensure_one()
        ticket = self.env['helpdesk.ticket'].create({
            'name': self.name,
            'description': self.description,
            'tag_ids': [(6, 0, [self.tag_id.id])] if self.tag_id else False,
        })
        
        # Save the ticket in the wizard
        self.ticket_id = ticket

        # Next step of the wizard
        self.state = 'step_2'

        # Return the action to reload the wizard form
        return {
            'type': 'ir.actions.act_window',
            'res_model': 'helpdesk.create.ticket',
            'res_id': self.id,
            'view_mode': 'form',
            'target': 'new',
        }
    
    def view_ticket(self):
        # Open the created ticket in form view
        return {
            'name': _('Ticket'),
            'view_mode': 'form',
            'res_model': 'helpdesk.ticket',
            'res_id': self.ticket_id.id,
            'type': 'ir.actions.act_window',
        }