from odoo import fields, models

class ResUsers(models.Model):
    _inherit = 'res.users'
    
    #Pour le premier bonus : auto assign manager : every time a user approve a sale.order, we can increment a integer field
    counter_approved_sale_order = fields.Integer(string="Number of approved sale order")