import frappe
from erpnext.accounts.report.profit_and_loss_statement.profit_and_loss_statement import execute as original_execute

def execute(filters=None):
    # Get original data
    columns, data, message, chart, report_summary = original_execute(filters)
    
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
            fc_amount = get_fc_amount(row.get('account'), filters)
            row['amount_fc'] = fc_amount
    
    # Ensure chart data is properly formatted
    if chart:
        # Ensure datasets have valid values (replace None/null with 0)
        for dataset in chart.get('data', {}).get('datasets', []):
            dataset['values'] = [float(v) if v is not None else 0.0 for v in dataset.get('values', [])]
        
        # Ensure chart type is valid
        if not chart.get('type'):
            chart['type'] = 'line'
            
        # Ensure chart has valid labels
        if not chart.get('data', {}).get('labels'):
            chart['data']['labels'] = ['']
    else:
        # Provide default chart if none exists
        chart = {
            "data": {
                "labels": [''],
                "datasets": [{
                    "name": "Income",
                    "values": [0.0]
                }]
            },
            "type": "line"
        }
    
    return columns, data, message, chart, report_summary

def get_fc_amount(account, filters):
    if not account or not filters:
        return 0
        
    sql = """
        SELECT 
            SUM(debit_in_account_currency) - SUM(credit_in_account_currency) as fc_balance
        FROM `tabGL Entry`
        WHERE 
            account=%s 
            AND posting_date BETWEEN %s AND %s
            AND docstatus = 1
    """
    
    try:
        fc_amount = frappe.db.sql(
            sql, 
            (account, filters.get('from_date'), filters.get('to_date')), 
            as_dict=True
        )
        return fc_amount[0].fc_balance if fc_amount and fc_amount[0].fc_balance else 0
    except Exception as e:
        frappe.log_error(f"Error getting FC amount for {account}: {str(e)}")
        return 0
