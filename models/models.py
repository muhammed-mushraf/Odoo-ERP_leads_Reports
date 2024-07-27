from odoo import models, fields, api


class CrmLead(models.Model):
    _inherit = 'crm.lead'

    def won_leads_count(self):
        print('rnewrfuewk')
        won_leads = self.env['crm.lead'].search_count([('stage_id.name', '=', 'Won')])
        return won_leads

    def lost_leads_count(self):
        print('rnewrfuewk')
        lost_leads = self.env['crm.lead'].search_count([('active', '=', False)])
        return lost_leads
