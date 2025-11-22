from odoo import api, Command, fields, models
from odoo.exceptions import UserError

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
    # assigned = fields.Boolean(
    #     readonly=True
    # )
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
    
    # Method to update a ticket's description
    def update_description(self):
        self.write({'description':"UPDATED"})

    # Many to many field
    tag_ids = fields.Many2many(
        'helpdesk.ticket.tag', 
        # relation='helpdesk_ticket_tag_rel',
        # column1='ticket_id',
        # column2='tag_id',
        string='Tags')

    # One to many field
    action_ids = fields.One2many(
        'helpdesk.ticket.action', 
        'ticket_id', 
        string='Actions')
    
    def set_actions_as_done(self):
        self.ensure_one()
        self.action_ids.set_done()

    color = fields.Integer('Color Index', default=0)

    amount_time = fields.Float(
        string='Amount of Time'
    )

    # Test domain
    person_id = fields.Many2one('res.partner', 
    string='Person ID',
    domain=[('is_company', '=', False)]
    )

    # Hacer que el campo assigned sea calculado, 
    # Hacer que se pueda busca con el atributo search 
    # Hacer que se pueda modificar de forma que si lo marco se actualice el usuario con el usuario conectado
    # si lo desmarco se limpie el campo del usuario
    assigned = fields.Boolean(
        compute='_compute_assigned', 
        string='assigned',
        search='_search_assigned',
        inverse='_inverse_assigned',
    )
    
    @api.depends('user_id')
    def _compute_assigned(self):
        
        # Método compute que calcula el valor del campo 'assigned'
        # basándose en si existe o no un usuario asignado
        

        # Itera sobre cada registro del recordset
        for record in self:
            # Asigna True al campo 'assigned' si user_id tiene un valor (no es False/None)
            # Asigna False si user_id está vacío
            record.assigned = bool(record.user_id)

    def _search_assigned(self, operator, value):
        
        # Método search personalizado para el campo 'assigned'
        # Permite buscar registros usando el campo computed 'assigned'
        # en filtros y búsquedas de Odoo
    
        # Args:
        #     operator: operador de búsqueda ('=', '!=', etc.)
        #     value: valor a buscar (True o False)
        
        # Validación de parámetros de entrada para el método _search_assigned
        
        # Verifica que:
        # 1. El operador sea '=' o '!=' (operadores válidos para campos booleanos)
        # 2. El valor sea de tipo booleano (True o False)
    
        # Si alguna condición no se cumple, lanza un error
        
        if operator not in ('=', '!=') or not isinstance(value, bool):
            # Lanza una excepción UserError (error visible para el usuario en Odoo)
            # indicando que la operación de búsqueda no está soportada
            raise UserError(("Operation not supported"))
        # Si se busca assigned = True (registros asignados)
        if operator == '=' and value == True:
            # Invertimos la lógica: buscamos donde user_id NO sea False
            operator = '!='
        else:
            # En cualquier otro caso (assigned = False, assigned != True, etc.)
            # Buscamos donde user_id SÍ sea False (sin asignar)
            operator = '='
        # Retorna el dominio de búsqueda traducido
        # Si assigned=True → busca user_id != False (con usuario)
        # Si assigned=False → busca user_id = False (sin usuario)
        return[('user_id', operator, False)]
    
    def _inverse_assigned(self):
        
        # Método inverse que permite escribir/modificar directamente el campo computed 'assigned'
        # y que automáticamente actualice el campo relacionado 'user_id'
    
        # Este método se ejecuta cuando alguien asigna un valor al campo 'assigned'
        # Por ejemplo: record.assigned = True o record.assigned = False
        
            for record in self:
                # Si se desmarca 'assigned' (se pone en False)
                if not record.assigned:
                    # Limpia el campo user_id (lo pone en False/vacío)
                    # Esto significa "desasignar el usuario"
                    record.user_id = False
                else:
                    # Si se marca 'assigned' (se pone en True)
                    # Asigna automáticamente el usuario actual (quien está haciendo la operación)
                    # self.env.user es el usuario logueado en Odoo
                    record.user_id = self.env.user

    
    # - Hacer un campo calculado que indique, dentro de un ticket, la cantidad de tickets asociados al mismo usuario.
    tickets_count = fields.Integer(
        string='Tickets Count',
        compute='_compute_tickets_count'
    )

    @api.depends('user_id')
    def _compute_tickets_count(self):
        ticket_obj = self.env['helpdesk.ticket']
        for record in self:
            tickets = ticket_obj.search([('user_id', '=', record.user_id.id)])
            record.tickets_count = len(tickets)

    # - Crear un campo nombre de etiqueta y hacer un botón que cree la nueva etiqueta con ese nombre y lo asocie al ticket.
    tag_name = fields.Char()

    def create_tag(self):
        self.ensure_one()
        # self.write({
        #     'tag_ids': [Command.create({'name': self.tag_name})] # Use this when there are mutiple records
        # })
        self.tag_ids = [Command.create({'name': self.tag_name})]  # Use this when only one record is being processed
        # we use tags_ids cause create returns a recordset of ids

    def clear_tags(self):
        # self.write({
        #     'tag_ids': [(5, 0, 0)]  Ancient way to clear tags odoo version 14 and before
        # })
        
        # Alternative way to clear tags using Command
        self.write({
            'tag_ids': [Command.clear()]  # Clears all tags associated with the ticket  
        })
