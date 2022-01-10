# -*- coding: utf-8 -*-

from odoo import models, fields, api
import inflect

class EditInvoice(models.Model):
    _inherit = 'account.move.line'
    
    word_subtotal = fields.Char(compute='compute_char')
    word_tax = fields.Char(compute='compute_char_tax')
    
    api.depends("word_subtotal", "price_subtotal")
    def compute_char(self):
        p = inflect.engine()
        
        self.word_subtotal = f"{p.number_to_words(self.price_subtotal)} {self.currency_id.name}"
    
    api.depends("word_subtotal", "tax_ids")
    def compute_char_tax(self):
        p = inflect.engine()
        
        self.word_tax = f"{p.number_to_words(((self.tax_ids.amount*self.price_subtotal)/100)*1515)} LBP"
