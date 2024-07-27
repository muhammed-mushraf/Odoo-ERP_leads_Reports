# -*- coding: utf-8 -*-
from odoo import models, fields, api
from datetime import datetime, timedelta


class CrmLead(models.TransientModel):
    _name = 'wizard.crmlead'

    from_date = fields.Date(string="From")
    to_date = fields.Date(string="To")

    def excel_report(self):
        return self.env.ref('dgz_crm_leads_reports.wizard_lead_report_xlsx').report_action(self)

    def pdf_report(self):
        domain = [
            ('create_date', '>=', self.from_date),
            ('create_date', '<=', self.to_date),
            ('active', 'in', [True, False])
        ]

        leads = self.env['crm.lead'].search(domain)

        won_leads_count = 0
        lost_leads_count = 0
        leads_data = []
        salespersons = {}

        for lead in leads:
            lead_dict = {
                'salesperson': lead.user_id.name,
                'lead_name': lead.name,
                'expected_revenue': lead.expected_revenue,
                'customer': lead.partner_id.name,
                'email': lead.partner_id.email,
                'phone': lead.partner_id.phone,
                'expected_closing': lead.date_deadline,
                'priority': lead.priority,
                'tags': [tag.name for tag in lead.tag_ids],
                'status': 'Lost' if not lead.active else lead.stage_id.name,
                'lost_reason': lead.lost_reason_id.name,
            }
            leads_data.append(lead_dict)

            if lead.stage_id and lead.stage_id.name == 'Won':
                won_leads_count += 1
            elif not lead.active:
                lost_leads_count += 1

            # Organize data by salesperson
            if lead.user_id.name not in salespersons:
                salespersons[lead.user_id.name] = {
                    'total_leads': 0,
                    'won_leads': 0,
                    'lost_leads': 0,
                }
            salespersons[lead.user_id.name]['total_leads'] += 1
            if lead.stage_id and lead.stage_id.name == 'Won':
                salespersons[lead.user_id.name]['won_leads'] += 1
            elif not lead.active:
                salespersons[lead.user_id.name]['lost_leads'] += 1

        # Define leads_past_90_days here
        leads_past_90_days = self.env['crm.lead'].search([
            ('create_date', '>=', (datetime.now() - timedelta(days=90)).strftime('%Y-%m-%d')),
            ('create_date', '<', self.from_date),
            ('active', 'in', [True, False])
        ])

        # Calculate won and lost leads from the past 90 days for each user
        won_leads_past_90_days = {}
        lost_leads_past_90_days = {}
        for lead_past_90_days in leads_past_90_days:
            user_name = lead_past_90_days.user_id.name
            if user_name not in won_leads_past_90_days:
                won_leads_past_90_days[user_name] = 0
            if user_name not in lost_leads_past_90_days:
                lost_leads_past_90_days[user_name] = 0

            if lead_past_90_days.stage_id and lead_past_90_days.stage_id.name == 'Won':
                won_leads_past_90_days[user_name] += 1
            elif not lead_past_90_days.active:
                lost_leads_past_90_days[user_name] += 1

        # Now you have the counts and leads_data, you can use them as needed
        print("Won Leads Count:", won_leads_count)
        print("Lost Leads Count:", lost_leads_count)
        print("Salespersons Data:", salespersons)
        print("Won Leads from Past 90 Days:", won_leads_past_90_days)
        print("Lost Leads from Past 90 Days:", lost_leads_past_90_days)

        data = {
            'from_date': self.from_date,
            'to_date': self.to_date,
            'leads_data': leads_data,
            'won_leads_count': won_leads_count,
            'lost_leads_count': lost_leads_count,
            'salespersons': salespersons,
            'won_leads_past_90_days': won_leads_past_90_days,
            'lost_leads_past_90_days': lost_leads_past_90_days,
        }

        return self.env.ref('dgz_crm_leads_reports.wizard_lead_report').report_action(leads.ids, data)

    def cancel_report(self):
        return True
