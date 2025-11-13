from odoo import fields, models

# Defines a new class (model) that represents a database table in Odoo
class HelpdeskTicket(models.Model):
    # Technical name of the model used internally by Odoo
    _name = 'helpdesk.ticket'
    # Human-readable description of the model
    _description = 'Helpdesk Ticket'
    
    # Nombre -> Char -> single-line text
    name = fields.Char()

    # Descripción - > Text -> multi-line text
    description = fields.Text()

    # Fecha
    date = fields.Date()

    # Fecha y Hora límite
    date_limit = fields.Datetime('Limit Date & Time')

    # Asignado (Verdadero o Falso)
    assigned = fields.Boolean()

    # Acciones a realizar
    actions_todo = fields.Html()