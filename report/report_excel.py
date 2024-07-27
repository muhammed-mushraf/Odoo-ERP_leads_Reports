# -*- coding: utf-8 -*-
from odoo import models


class WizardLeadXlsx(models.AbstractModel):
    _name = 'report.dgz_crm_leads_reports.report_wizard_xls'
    _inherit = 'report.report_xlsx.abstract'

    def get_priority_label(self, priority):
        priority_labels = {
            '0': 'Not set',
            '1': 'Low',
            '2': 'Medium',
            '3': 'High',
        }
        return priority_labels.get(priority, '')

    def generate_xlsx_report(self, workbook, data, dgz_crm_leads_reports):
        format1 = workbook.add_format({'font_size': 10, 'align': 'vcenter', 'bold': True})
        format2 = workbook.add_format({'font_size': 10, 'align': 'vcenter'})
        sheet = workbook.add_worksheet('Leads Report')
        sheet.set_column(0, 0, 15)
        sheet.set_column(1, 1, 25)
        sheet.set_column(2, 2, 20)
        sheet.set_column(3, 3, 25)
        sheet.set_column(4, 4, 25)
        sheet.set_column(5, 5, 15)
        sheet.set_column(6, 6, 15)
        sheet.set_column(7, 7, 10)
        sheet.set_column(8, 8, 20)
        sheet.set_column(9, 9, 15)
        sheet.set_column(10, 10, 20)

        # Get data from the context
        from_date = dgz_crm_leads_reports.from_date
        to_date = dgz_crm_leads_reports.to_date

        # Search leads based on date range
        domain = [
            ('create_date', '>=', from_date),
            ('create_date', '<=', to_date),
            ('active', 'in', [True, False])

        ]

        leads = self.env['crm.lead'].search(domain)
        print(len(leads),'leaddddddddddddddddddd')
        # Create a worksheet and write headers
        sheet.write(0, 0, 'Sales Person', format1)
        sheet.write(0, 1, 'Lead Name', format1)
        sheet.write(0, 2, 'Expected Revenue', format1)
        sheet.write(0, 3, 'Customer', format1)
        sheet.write(0, 4, 'Email', format1)
        sheet.write(0, 5, 'Phone', format1)
        sheet.write(0, 6, 'Expected closing', format1)
        sheet.write(0, 7, 'Priority', format1)
        sheet.write(0, 8, 'Tags', format1)
        sheet.write(0, 9, 'Status', format1)
        sheet.write(0, 10, 'Lost Reason', format1)

        # Populate data in the worksheet
        row = 1
        won_leads_count = 0
        lost_leads_count = 0
        for lead in leads:
            sheet.write(row, 0, lead.user_id.name if lead.user_id else '', format2)
            sheet.write(row, 1, lead.name, format2)
            sheet.write(row, 2, lead.expected_revenue, format2)
            sheet.write(row, 3, lead.partner_id.name if lead.partner_id else '', format2)
            sheet.write(row, 4, lead.email_from, format2)
            sheet.write(row, 5, lead.phone, format2)
            sheet.write(row, 6, lead.date_deadline, format2)

            # Convert priority to label using the mapping function
            priority_label = self.get_priority_label(lead.priority)
            sheet.write(row, 7, priority_label, format2)

            tags = ', '.join(tag.name for tag in lead.tag_ids) if lead.tag_ids else ''
            sheet.write(row, 8, tags, format2)
            sheet.write(row, 9, lead.stage_id.name if lead.stage_id else '', format2)
            sheet.write(row, 10, lead.lost_reason_id.name if lead.lost_reason_id else '', format2)

            if lead.stage_id and lead.stage_id.name == 'Won':
                won_leads_count += 1
            elif not lead.active:  # Count as "lost" if lead is not active
                sheet.write(row, 9, 'Lost', format2)
                sheet.write(row, 10, lead.lost_reason_id.name if lead.lost_reason_id else '', format2)
                lost_leads_count += 1

            row += 1
        row += 2

        # Add a thank-you message after the gap

        sheet.write(row + 1, 0, 'Total Won Leads', format1)
        sheet.write(row + 1, 1, won_leads_count, format2)
        sheet.write(row + 2, 0, 'Total Lost Leads', format1)
        sheet.write(row + 2, 1, lost_leads_count, format2)

        # Add a line break before the 'SalesPerson Record Details' text
        row += 3  # Adjust the row index to eliminate the gap


        # Move to the next line for headers
        row += 2

        sheet.write(row, 0, 'Sales Person', format1)
        sheet.write(row, 1, 'Total Leads', format1)
        sheet.write(row, 2, 'Won Leads', format1)
        sheet.write(row, 3, 'Lost Leads', format1)

        # Populate SalesPerson Record Details data in the worksheet
        salesperson_leads_count = {}  # Dictionary to store counts for each salesperson
        for lead in leads:
            salesperson_name = lead.user_id.name if lead.user_id else 'Not Assigned'
            if salesperson_name not in salesperson_leads_count:
                salesperson_leads_count[salesperson_name] = {'total': 0, 'won': 0, 'lost': 0}

            # Increment the total count for the salesperson
            salesperson_leads_count[salesperson_name]['total'] += 1

            # Increment the count based on lead status (won/lost)
            if lead.stage_id and lead.stage_id.name == 'Won':
                salesperson_leads_count[salesperson_name]['won'] += 1
            elif not lead.active:  # Count as "lost" if lead is not active
                salesperson_leads_count[salesperson_name]['lost'] += 1

        # Populate SalesPerson Record Details data in the worksheet
        salesperson_row = row + 1
        for salesperson, counts in salesperson_leads_count.items():
            sheet.write(salesperson_row, 0, salesperson, format2)
            sheet.write(salesperson_row, 1, counts['total'], format2)
            sheet.write(salesperson_row, 2, counts['won'], format2)
            sheet.write(salesperson_row, 3, counts['lost'], format2)

            salesperson_row += 1
