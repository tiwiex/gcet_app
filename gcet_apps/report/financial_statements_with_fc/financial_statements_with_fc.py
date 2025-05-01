from __future__ import unicode_literals
import frappe
from frappe import _
from erpnext.accounts.report.financial_statements import (
    get_period_list,
    get_columns,
    get_data,
    get_filtered_list_for_consolidated_report
)

def execute(filters=None):
    if not filters.get("company"):
        frappe.throw(_("Company is required"))
    if not filters.get("secondary_currency"):
        frappe.throw(_("Secondary Currency is required"))
        
    period_list = get_period_list(
        filters.from_date,
        filters.to_date,
        filters.period_length,
        filters.accumulated_values
    )
    
    # Get base report data
    income = get_data(
        filters.company,
        "Income",
        "Credit",
        period_list,
        filters=filters,
        accumulated_values=filters.accumulated_values,
        ignore_closing_entries=True,
        ignore_accumulated_values_for_fy=True
    )

    # Add FC columns
    columns = get_columns(filters.company, period_list, filters.report_type)
    columns = add_fc_columns(columns, filters.secondary_currency)
    
    # Convert amounts
    data = convert_data_to_fc(income, filters)
    
    return columns, data, None, None

def add_fc_columns(columns, currency):
    new_columns = []
    for col in columns:
        new_columns.append(col)
        if col.get("fieldtype") == "Currency":
            fc_col = col.copy()
            fc_col["fieldname"] = f"{col['fieldname']}_fc"
            fc_col["label"] = f"{col['label']} ({currency})"
            fc_col["options"] = currency
            new_columns.append(fc_col)
    return new_columns

def convert_data_to_fc(data, filters):
    if not data:
        return data
        
    company_currency = frappe.get_cached_value(
        "Company", filters.company, "default_currency"
    )
    exchange_rate = get_exchange_rate(
        company_currency,
        filters.secondary_currency,
        filters.to_date
    )
    
    for row in data:
        for key in row:
            if isinstance(row[key], (float, int)):
                row[f"{key}_fc"] = row[key] / exchange_rate
    return data

def get_exchange_rate(from_currency, to_currency, date):
    if from_currency == to_currency:
        return 1.0
    
    rate = frappe.db.get_value(
        "Currency Exchange",
        {
            "from_currency": from_currency,
            "to_currency": to_currency,
            "date": ["<=", date]
        },
        "exchange_rate",
        order_by="date desc"
    )
    
    if not rate:
        frappe.throw(
            _(f"No exchange rate found for {from_currency} to {to_currency} on or before {date}")
        )
    
    return rate
