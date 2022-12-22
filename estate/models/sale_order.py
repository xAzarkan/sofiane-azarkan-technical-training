from odoo import api, models, _, fields
from odoo.exceptions import ValidationError
from datetime import timedelta



class SaleOrder(models.Model):
    _inherit = 'sale.order'

    
    def action_confirm(self):
        # Get the current connected user
        current_user = self.env.user

        max_amount = self.get_max_amount_value('Manager Level 2')

        if self.amount_total <= max_amount:
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

            # Call the super method to confirm the sale order
            return super(SaleOrder, self).action_confirm()

        else:
            #return self.message_post(body=f'Sale order can not be confirmed by {current_user.name}')
            raise TimeoutError(f"Sale order can not be confirmed by {current_user.name}")


    def get_max_amount_value(self, group_name):

        current_user = self.env.user
        groups = current_user.groups_id

        for group in groups:
            if group.max_amount:
                return group.max_amount

        return 

        # # Search for the group by name
        # group_ids = self.env['res.groups'].search([('name', '=', group_name)])
        # # Get the group record
        # group = self.env['res.groups'].browse(group_ids)
        # # Get the value of the field
        # return group.max_amount
        # # Do something with the field value
        # #print(field_value)

        # # Récupération des groupes de l'utilisateur
        # groups = user.groups_id

        # # Initialisation du niveau de gestionnaire de l'utilisateur à 0
        # user_level = 0

        # # Vérification du niveau de gestionnaire de l'utilisateur
        # for group in groups:
        #     if group.max_amount:
        #         user_level = max(user_level, group.max_amount)

    
