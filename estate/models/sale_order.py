from odoo import api, models, _, fields
from odoo.exceptions import ValidationError

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        # Call the super method to confirm the sale order
        res = super(SaleOrder, self).action_confirm()

        # Iterate over the sale order lines
        for line in self.order_line:
            # Check if the training date is set
            if line.training_date:
                # Create a new event in the calendar for the selected employee
                self.env['calendar.event'].create({
                    'name': 'Training',
                    'start_date': line.training_date,
                    'stop_date': line.training_date + timedelta(hours=8),
                    'allday': True,
                    'partner_ids': [(6, 0, [self.partner_id.id])],
                })

        return res