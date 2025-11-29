# - Hacer un test para comprobar que si intento poner dedicated_time negativo me lanza una expcepción.

from odoo import fields
from odoo.exceptions import UserError
from odoo.tests.common import TransactionCase

class TestHelpdeskTicket(TransactionCase):
    @classmethod
    # Set up the test class by creating a helpdesk ticket and referencing the admin user
    def setUpClass(self):
        super().setUpClass()
        self.ticket = self.env['helpdesk.ticket'].create({
            'name': 'Test ticket',
            'description': 'Test description',
        })
        self.user_admin = self.env.ref('base.user_admin')
    
    # Test to ensure that setting a negative value for amount_time raises a UserError
    def test_ticket_amount_time_no_negative(self):
        self.ticket.amount_time = 3
        self.assertEqual(self.ticket.amount_time, 3, "The amount_time should be 3 hours.")
        with self.assertRaises(UserError):
            self.ticket.amount_time = -1
    
    # Test to ensure that the assigned field behaves correctly when user_id is set or unset
    def test_ticket_assigned(self):
        self.assertFalse(self.ticket.assigned, "The ticket should not be assigned initially.")
        self.ticket.user_id = self.user_admin
        self.assertTrue(self.ticket.assigned, "The ticket should be assigned after setting user_id.")
        self.ticket.user_id = False
        self.assertFalse(self.ticket.assigned, "The ticket should not be assigned after unsetting user_id.")
    
    # Test to ensure that searching by the assigned field works as expected
    def test_ticket_search_assigned(self):
        self.assertIn(self.ticket, self.env['helpdesk.ticket'].search([('assigned', '=', False)]), "The ticket should be found when searching for unassigned tickets.")
        self.assertIn(self.ticket, self.env['helpdesk.ticket'].search([('assigned', '!=', True)]), "The ticket should be found when searching for tickets not assigned.")
        self.ticket.user_id = self.user_admin
        self.assertIn(self.ticket, self.env['helpdesk.ticket'].search([('assigned', '=', True)]), " The ticket should be found when searching for assigned tickets.")
        self.assertIn(self.ticket, self.env['helpdesk.ticket'].search([('assigned', '!=', False)]), "The ticket should be found when searching for tickets that are assigned.")
        with self.assertRaises(UserError):
            self.env['helpdesk.ticket'].search([('assigned', '>', True)])


    