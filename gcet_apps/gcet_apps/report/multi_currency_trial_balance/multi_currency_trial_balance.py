# Copyright (c) 2024, Taiwo Akinosho and contributors
# For license information, please see license.txt

from __future__ import unicode_literals
import frappe
from frappe import _
from frappe.utils import flt, get_currency_precision

def execute(filters=None):
    if not filters:
        filters = {}
    
    validate_filters(filters)
    columns = get_columns(filters)
    data = get_data(filters)
    
    return columns, data

def validate_filters(filters):
    if not filters.get('company'):
        frappe.throw(_("Company is required"))
    if not filters.get('from_date'):
        frappe.throw(_("From Date is required"))
    if not filters.get('to_date'):
        frappe.throw(_("To Date is required"))
    if not filters.get('secondary_currency'):
        frappe.throw(_("Secondary Currency is required"))

def get_columns(filters):
    company_currency = frappe.get_cached_value('Company', filters.get('company'), 'default_currency')
    secondary_currency = filters.get('secondary_currency')
    
    return [
        {
            "label": _("Account"),
            "fieldname": "account",
            "fieldtype": "Link",
            "options": "Account",
            "width": 300
        },
        {
            "label": _("Account Type"),
            "fieldname": "account_type",
            "fieldtype": "Data",
            "width": 150
        },
        {
            "label": _("Debit ({})").format(company_currency),
            "fieldname": "debit",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150
        },
        {
            "label": _("Credit ({})").format(company_currency),
            "fieldname": "credit",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150
        },
        {
            "label": _("Balance ({})").format(company_currency),
            "fieldname": "balance",
            "fieldtype": "Currency",
            "options": "currency",
            "width": 150
        },
        {
            "label": _("Debit ({})").format(secondary_currency),
            "fieldname": "debit_secondary",
            "fieldtype": "Currency",
            "options": "secondary_currency",
            "width": 150
        },
        {
            "label": _("Credit ({})").format(secondary_currency),
            "fieldname": "credit_secondary",
            "fieldtype": "Currency",
            "options": "secondary_currency",
            "width": 150
        },
        {
            "label": _("Balance ({})").format(secondary_currency),
            "fieldname": "balance_secondary",
            "fieldtype": "Currency",
            "options": "secondary_currency",
            "width": 150
        }
    ]

def get_data(filters):
    gl_entries = get_gl_entries(filters)
    accounts = get_accounts_with_balances(gl_entries, filters)
    
    data = []
    for acc in accounts:
        if not filters.get('show_zero_balance') and not (acc.debit or acc.credit):
            continue
            
        row = {
            "account": acc.name,
            "account_type": acc.account_type,
            "debit": acc.debit,
            "credit": acc.credit,
            "balance": acc.balance,
            "debit_secondary": acc.debit_secondary,
            "credit_secondary": acc.credit_secondary,
            "balance_secondary": acc.balance_secondary,
            "currency": filters.get('company_currency'),
            "secondary_currency": filters.get('secondary_currency')
        }
        data.append(row)
    
    return data

def get_gl_entries(filters):
    return frappe.db.sql("""
        SELECT 
            gl.account,
            gl.debit,
            gl.credit,
            gl.debit_in_account_currency,
            gl.credit_in_account_currency,
            gl.account_currency,
            acc.account_type,
            acc.root_type
        FROM `tabGL Entry` gl
        JOIN `tabAccount` acc ON gl.account = acc.name
        WHERE gl.company = %(company)s
            AND gl.posting_date BETWEEN %(from_date)s AND %(to_date)s
            AND gl.docstatus = 1
            AND gl.is_cancelled = 0
    """, filters, as_dict=1)

def get_accounts_with_balances(gl_entries, filters):
    accounts = {}
    company_currency = frappe.get_cached_value('Company', filters.get('company'), 'default_currency')
    
    for entry in gl_entries:
        if entry.account not in accounts:
            accounts[entry.account] = frappe._dict({
                "name": entry.account,
                "account_type": entry.account_type,
                "debit": 0,
                "credit": 0,
                "debit_secondary": 0,
                "credit_secondary": 0,
                "balance": 0,
                "balance_secondary": 0
            })
            
        acc = accounts[entry.account]
        
        # Primary currency
        acc.debit += flt(entry.debit)
        acc.credit += flt(entry.credit)
        acc.balance = acc.debit - acc.credit
        
        # Secondary currency
        if entry.account_currency == filters.get('secondary_currency'):
            acc.debit_secondary += flt(entry.debit_in_account_currency)
            acc.credit_secondary += flt(entry.credit_in_account_currency)
        else:
            # Convert to secondary currency using exchange rate
            exchange_rate = get_exchange_rate(company_currency, filters.get('secondary_currency'))
            acc.debit_secondary += flt(entry.debit * exchange_rate)
            acc.credit_secondary += flt(entry.credit * exchange_rate)
        
        acc.balance_secondary = acc.debit_secondary - acc.credit_secondary
    
    return accounts.values()

def get_exchange_rate(from_currency, to_currency):
    rate = frappe.db.get_value("Currency Exchange", 
        {"from_currency": from_currency, "to_currency": to_currency},
        "exchange_rate")
    return flt(rate) if rate else 1.0
