import frappe
from erpnext.accounts.report.balance_sheet.balance_sheet import execute as original_execute

def execute(filters=None):
    # Get original data
    columns, data, message, chart, report_summary, primitive_summary = original_execute(filters)
    
    # Add FC column after the first amount column
    columns.insert(2, {
        "fieldname": "amount_fc",
        "label": "Amount (FC)",
        "fieldtype": "Currency",
        "options": "currency",
        "width": 120
    })
    
    # Add FC values to data
    for row in data:
        if isinstance(row, dict) and row.get('account'):
            # Get FC amount logic here
            fc_amount = get_fc_amount(row.get('account'), filters)
            row['amount_fc'] = fc_amount
    
    return columns, data, message, chart, report_summary, primitive_summary

def get_fc_amount(account, filters):
    # Add your logic to get FC amount
    # This is just an example - implement your actual FC calculation
    sql = """
        SELECT SUM(debit_in_account_currency) - SUM(credit_in_account_currency) as fc_balance
        FROM `tabGL Entry`
        WHERE account=%s AND posting_date <= %s
    """
    fc_amount = frappe.db.sql(sql, (account, filters.get('to_date')), as_dict=True)
    return fc_amount[0].fc_balance if fc_amount else 0
