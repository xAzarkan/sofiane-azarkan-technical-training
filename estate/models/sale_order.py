from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
   
    @api.multi
    def confirm(self):
        # Call the original confirm method to complete the sale order confirmation process
        super().confirm()

        # Retrieve the calendar of the selected employee
        employee = self.employee_id
        calendar = employee.resource_calendar_id

        # Create a new event in the calendar
        event_vals = {
            'name': self.name,
            'start': self.date_order,
            'stop': self.date_order + timedelta(hours=8),
            'allday': False,
            'resource_id': calendar.id,
        }
        event = self.env['calendar.event'].create(event_vals)