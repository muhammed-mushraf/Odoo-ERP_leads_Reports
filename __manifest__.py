{
    'name': 'dgz Crm lead reports',
    'depends': ['base','crm', 'report_xlsx'],
    'data': [
        'security/ir.model.access.csv',
        'views/wizard_crmlead.xml',
        'report/pdf_report.xml',
        'report/pdf_report_template.xml',
        'report/report_excel.xml',
    ],
    'sequence': '4',
    'instalable': True,
    'application': True,
}
