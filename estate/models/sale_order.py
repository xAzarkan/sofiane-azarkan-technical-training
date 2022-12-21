from odoo import api, models, _, fields
from odoo.exceptions import ValidationError
from datetime import timedelta

class SaleOrder(models.Model):
    _inherit = 'sale.order'
    
    def action_confirm(self):
        current_user = self.env.user
        self.env.user.notification(message=f'Sale order confirmed by {current_user.name}')

        # Call the super method to confirm the sale order
        res = super(SaleOrder, self).action_confirm()

        # Iterate over the sale order lines
        for line in self.order_line:
            
            # Création d'un partenaire avec le nom de l'employé s'il n'a pas de partenaire associé
            if not line.employee_id.user_id:
                partner = self.env['res.partner'].create({
                    'name': line.employee_id.name,
                })
            else:
                partner = line.employee_id.user_id.partner_id

            # Check if the training date is set
            if line.training_date:
                # Create a new event in the calendar for the selected employee
                self.env['calendar.event'].create({
                    'name': 'Training for sale order',
                    'start_date': line.training_date,
                    'stop_date': line.training_date + timedelta(hours=8),
                    'allday': True,
                    'partner_ids': [(4, partner.id)],
                })

        return res