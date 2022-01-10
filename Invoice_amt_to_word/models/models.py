# -*- coding: utf-8 -*-

from odoo import models, fields, api
import inflect
from datetime import datetime

class EditInvoice(models.Model):
    _inherit = 'account.move'
    
    word_subtotal = fields.Char(compute='compute_char')
    word_tax = fields.Char(compute='compute_char_tax')
    tax_lbp = fields.Float()
    
    api.depends("word_subtotal", "price_subtotal")
    def compute_char(self):
        p = inflect.engine()
        
        self.word_subtotal = f"{p.number_to_words(self.amount_total)}"
    
    api.depends("word_tax", "amount_by_group")
    def compute_char_tax(self):
        p = inflect.engine()
        
        tax_unconverted = "{:.2f}".format((self.amount_total - self.amount_untaxed))
        
        lbp_currency = self.env['res.currency'].search([('name', '=', 'LBP')])
        
        convert_to_lbp = self.env['res.currency'].browse(self.currency_id.id)._convert(float(tax_unconverted), lbp_currency, self.company_id, datetime.today())
        
        tax_total = "{:.2f}".format(float(convert_to_lbp))
        self.tax_lbp = tax_total
        self.word_tax = f"{p.number_to_words(float(tax_total))}"
