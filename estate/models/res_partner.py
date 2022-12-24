from odoo import fields, models

class ResPartner(models.Model):
    _inherit = 'res.partner'
    max_sale_order_amount = fields.Float(string="Maximum Sale Order Amount") #Création d'un nouveau champ dans la DB de type Float
    
    #Pour le premier bonus : auto assign manager : every time a user approve a sale.order, we can increment a integer field
    counter_approved_sale_order = fields.Integer(string="Number of approved sale order")