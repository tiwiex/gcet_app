import frappe
from erpnext.accounts.report.balance_sheet.balance_sheet import execute as original_execute
from frappe.utils import flt
from frappe import _
import logging
import json

# Set up logging
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)

def execute(filters=None):
    logger.info("Balance Sheet with USD execute called")
    logger.debug(f"Original filters: {filters}")
    
    try:
        # Ensure filters is a dictionary
        if isinstance(filters, str):
            filters = json.loads(filters)
        
        if not filters:
            filters = {}
            
        # Ensure periodicity is set
        if "periodicity" not in filters:
            filters["periodicity"] = "Yearly"
            
        logger.info(f"Using filters for original execute: {filters}")
        
        # Get original data
        columns, data, message, chart, report_summary = original_execute(filters)
        logger.info("Original data retrieved")
        
        # Get exchange rate
        exchange_rate = get_usd_exchange_rate()
        logger.info(f"Using USD exchange rate: {exchange_rate}")
        
        # Add USD columns
        new_columns = []
        for col in columns:
            new_columns.append(col)
            if isinstance(col, dict) and col.get("fieldname") and col.get("fieldname") != "account":
                usd_col = col.copy()
                usd_col["fieldname"] = f"{col['fieldname']}_usd"
                usd_col["label"] = f"{col['label']} (USD)"
                usd_col["options"] = "Currency"
                usd_col["currency"] = "USD"
                new_columns.append(usd_col)
        
        columns = new_columns
        
        # Add USD values to data
        for row in data:
            if isinstance(row, dict):
                for col in columns:
                    if isinstance(col, dict) and col.get("fieldname") and "_usd" in col.get("fieldname"):
                        original_fieldname = col.get("fieldname").replace("_usd", "")
                        if row.get(original_fieldname) is not None:
                            row[col.get("fieldname")] = flt(row.get(original_fieldname)) / exchange_rate
        
        logger.info("Balance Sheet with USD execution completed")
        return columns, data, message, chart, report_summary
        
    except Exception as e:
        logger.error(f"Error in balance sheet with USD: {str(e)}")
        frappe.log_error(f"Balance Sheet with USD Error: {str(e)}", "Balance Sheet with USD Report Error")
        frappe.throw(f"Error in balance sheet with USD: {str(e)}")

def get_usd_exchange_rate():
    # Get the latest exchange rate from Currency Exchange doctype
    exchange_rate = frappe.db.get_value(
        "Currency Exchange",
        {
            "from_currency": "NGN",
            "to_currency": "USD",
        },
        "exchange_rate",
        order_by="date desc"
    )
    
    if not exchange_rate:
        frappe.msgprint(_("USD Exchange rate not found. Using 1 as default."))
        return 1.0
        
    return float(exchange_rate) 