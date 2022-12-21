from odoo import fields, models, Command

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'
    training_date = fields.Date(string="Training date") #attention revoir le type
    employee_id = fields.Many2one('hr.employee', string='Employee')

            