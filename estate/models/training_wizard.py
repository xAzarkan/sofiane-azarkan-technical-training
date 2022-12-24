from odoo import models, fields

class TrainingWizard(models.TransientModel):
    _name = 'training.wizard'

    training_date = fields.Date(string='Date of Training', required=True)