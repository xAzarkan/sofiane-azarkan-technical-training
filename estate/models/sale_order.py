from odoo import api, models, _, fields
from odoo.exceptions import ValidationError
from datetime import timedelta



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def action_confirm(self):
        # Get the current connected user
        current_user = self.env.user
        partner = self.partner_id
        max_amount = self.get_max_amount_value()

        # Verify max amount of the group (2) AND max amount of the partner (3)
        if self.amount_total <= max_amount: 
            if self.amount_total <= partner.max_sale_order_amount or partner.max_sale_order_amount is None:
                # Iterate over the sale order lines
                for order in self.order_line:
                    # Création d'un partenaire avec le nom de l'employé s'il n'a pas de partenaire associé
                    if not order.employee_id.user_id:
                        partner = self.env['res.partner'].create({
                            'name': order.employee_id.name,
                        })
                    else:
                        partner = order.employee_id.user_id.partner_id

                    # Check if the training date is set
                    if order.training_date:
                        # Create a new event in the calendar for the selected employee
                        self.env['calendar.event'].create({
                            'name': 'Training for sale order',
                            'start_date': order.training_date,
                            'stop_date': order.training_date + timedelta(hours=8),
                            'allday': True,
                            'partner_ids': [(4, partner.id)],
                        })

                # Call the super method to confirm the sale order
                return super(SaleOrder, self).action_confirm()
            else:
                return self.message_post(body=f'Sale order can not be confirmed for the partner {partner.name}')    

        else:
            return self.message_post(body=f'Sale order can not be confirmed by {current_user.name}')
            #raise Exception(f"Sale order can not be confirmed by {current_user.name}")

    # 2

    def get_max_amount_value(self):

        current_user = self.env.user
        groups = current_user.groups_id

        max_amount = 500 # default max_amount

        for group in groups:
            if group.max_amount:
                max_amount = group.max_amount

        return max_amount

    # 4    

    def request_approval(self):
        # Search for the administrator (Mitchell Admin)
        administrator = self.env['res.users'].search([('name', '=', 'Mitchell Admin')])
        if administrator:
            # Set the user_id to the administrator's ID
            user_id = administrator.id
        else:
            # Set the user_id to the superuser's ID
            user_id = self.env.ref('base.user_root').id

        # Create an activity for a manager
        self.env['mail.activity'].create({
            'res_model_id': self.env.ref('sale.model_sale_order').id,
            'res_id': self.id,
            'summary': _('Approval Requested'),
            'user_id': user_id,
        })
    
