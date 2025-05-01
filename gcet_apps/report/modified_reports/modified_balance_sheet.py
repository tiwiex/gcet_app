import frappe
from erpnext.accounts.report.balance_sheet.balance_sheet import execute as original_execute
import logging

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

# Fixed exchange rate for USD conversion (can be moved to settings later)
EXCHANGE_RATE = 1.5  # 1 FC = 1.5 USD

def execute(filters=None):
    logger.info("Modified balance sheet execute called")
    logger.debug(f"Filters: {filters}")
    
    try:
        # Get original data
        columns, data, message, chart, report_summary, primitive_summary = original_execute(filters)
        logger.info("Original data retrieved")
        
        # Add FC column after the first amount column
        columns.insert(2, {
            "fieldname": "amount_fc",
            "label": "Amount (FC)",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120
        })
        logger.info("FC column added")
        
        # Add USD column after FC column
        columns.insert(3, {
            "fieldname": "amount_usd",
            "label": "Amount (USD)",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 120,
            "convertible": "rate"
        })
        logger.info("USD column added")
        
        # Add FC and USD values to data
        for row in data:
            if isinstance(row, dict) and row.get('account'):
                logger.debug(f"Processing account: {row.get('account')}")
                # Get FC amount
                fc_amount = get_fc_amount(row.get('account'), filters)
                row['amount_fc'] = fc_amount
                
                # Calculate USD equivalent
                if fc_amount is not None:
                    usd_amount = fc_amount * EXCHANGE_RATE
                    row['amount_usd'] = usd_amount
                    logger.debug(f"Account {row.get('account')}: FC={fc_amount}, USD={usd_amount}")
                else:
                    row['amount_usd'] = None
                    logger.debug(f"Account {row.get('account')}: No FC amount found")
            elif isinstance(row, dict) and 'total' in row.get('indent', ''):
                # For total rows, calculate FC and USD from child rows
                fc_total = sum(float(child.get('amount_fc', 0)) for child in data if child.get('parent_account') == row.get('account'))
                row['amount_fc'] = fc_total
                if fc_total is not None:
                    row['amount_usd'] = fc_total * EXCHANGE_RATE
                    logger.debug(f"Total row {row.get('account')}: FC={fc_total}, USD={fc_total * EXCHANGE_RATE}")
                else:
                    row['amount_usd'] = None
                    logger.debug(f"Total row {row.get('account')}: No FC total found")
        
        logger.info("Modified balance sheet execution completed")
        return columns, data, message, chart, report_summary, primitive_summary
        
    except Exception as e:
        logger.error(f"Error in balance sheet modification: {str(e)}")
        frappe.throw(f"Error in balance sheet modification: {str(e)}")

def get_fc_amount(account, filters):
    logger.debug(f"Getting FC amount for account: {account}")
    """Get the foreign currency balance for the account."""
    sql = """
        SELECT 
            SUM(debit_in_account_currency) - SUM(credit_in_account_currency) as fc_balance,
            account_currency
        FROM `tabGL Entry`
        WHERE account = %s
        AND posting_date BETWEEN %s AND %s
        GROUP BY account_currency
    """
    
    result = frappe.db.sql(sql, (account, filters.from_date, filters.to_date), as_dict=True)
    logger.debug(f"SQL result for account {account}: {result}")
    
    if not result:
        logger.debug(f"No results found for account {account}")
        return None
        
    # Get the first currency result (assuming single currency per account)
    fc_balance = result[0].get('fc_balance')
    logger.debug(f"FC balance for account {account}: {fc_balance}")
    return fc_balance if fc_balance is not None else 0
