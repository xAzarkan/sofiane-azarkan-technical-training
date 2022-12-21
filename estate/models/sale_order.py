from odoo import api, models, _, fields
from odoo.exceptions import ValidationError
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        # Call the super method to confirm the sale order
        res = super(SaleOrder, self).action_confirm()

        for line in self.order_line:
            if line.training_date and line.employee_id:
                event_vals = {
                    'name': 'Training',
                    'start_date': line.training_date,
                    'stop_date': line.training_date + timedelta(hours=8),
                    'employee_id': line.employee_id.id,
                }
                self.env['calendar.event'].create(event_vals)        

        return res