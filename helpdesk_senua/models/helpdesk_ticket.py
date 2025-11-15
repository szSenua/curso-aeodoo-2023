from odoo import fields, models

# Defines a new class (model) that represents a database table in Odoo
class HelpdeskTicket(models.Model):
    # Technical name of the model used internally by Odoo
    _name = 'helpdesk.ticket'
    # Human-readable description of the model
    _description = 'Helpdesk Ticket'
    
    # Nombre -> Char -> single-line text
    name = fields.Char(
        required=True,
        help='Resume the title'
    )

    # Secuencia
    sequence = fields.Integer(
        default=10,
        help='Secuencia para el orden de las incidencias'
    )

    # Descripción - > Text -> multi-line text
    description = fields.Text()

    # Fecha
    date = fields.Date()

    # Fecha y Hora límite
    date_limit = fields.Datetime('Limit Date & Time')

    # Asignado (Verdadero o Falso)
    assigned = fields.Boolean(
        readonly=True
    )
    user_id = fields.Many2one('res.users', string='Assigned_to')

    # Acciones a realizar
    actions_todo = fields.Html()

    # Añadir el campo Estado [Nuevo, Asignado, En proceso, Pendiente, Resuelto, Cancelado], que por defecto sea Nuevo
    state = fields.Selection([
        ('new', 'New'),
        ('assigned', 'Assigned'),
        ('in_process', 'In Process'),
        ('pending', 'Pending'),
        ('resolved', 'Resolved'),
        ('canceled', 'Canceled')
        ],
    default= 'new',
    )

    # Provides the action used by the list-view button to open the record in form mode
    def action_open_form(self):
        """Open the form view of the selected ticket."""
        return {
            'type': 'ir.actions.act_window',   # Tells Odoo to open a window action
            'res_model': 'helpdesk.ticket',    # Model to open (this model)
            'res_id': self.id,                 # ID of the specific record clicked
            'view_mode': 'form',               # Open the record in form view
            'target': 'current',               # Replace the current screen (not open a popup)
    }
